import pymysql
import logging

class DataBase:
    __instance = None

    def __new__(cls):
        if DataBase.__instance is None:
            print('Conexión a la base de datos establecida')
            DataBase.__instance = object.__new__(cls)
        
        return DataBase.__instance

    def __init__(self):
        self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='root1234',
                database='signala'
            )
        
        self.cursor = self.connection.cursor()

    def insert(self, tabla: str, **kwargs) -> int:
        sql = 'INSERT INTO {}('.format(tabla)
        
        for dato in kwargs.items():
            sql += '{},'.format(dato[0])
        
        sql = sql[:-1] + ') VALUES ('
        for dato in kwargs.items():
            sql += r"'{}',".format(dato[1])
        
        sql = sql[:-1] + ')'
        
        logging.info('Realizando INSERT: '+sql)
        
        try:
            self.cursor.execute(sql)
        
        except pymysql.err.OperationalError as e:
            logging.warning("Error De Operacion: " + str(e))
            return 1
        except pymysql.err.IntegrityError as e:
            logging.info("Error de Integridad: " + str(e))
            return 2
        
        return 0

    def select(self, tabla: str, *args ,**kwargs) -> tuple[tuple, ...] | int:
        sql = 'SELECT '
        
        if len(args) == 0:
            sql += '* FROM {}'.format(tabla)
        else:
            for dato in args:
                sql += '{},'.format(dato)
            sql = sql[:-1] + ' FROM {}'.format(tabla)
        
        if len(kwargs) != 0:
            cont = 0
            for dato in kwargs.items():
                if cont == 0:
                    sql += ' WHERE '
                else:
                    sql = sql[:-1]
                    sql += ' AND '
                cont += 1
                
                if len(str(dato[1])) >= 2:
                    if str(dato[1])[0] == '%' or str(dato[1])[-1] == '%':
                        sql += r"{} LIKE '{}',".format(dato[0], dato[1])
                    else:
                        sql += r"{}='{}',".format(dato[0], dato[1])
                else:
                    sql += r"{}='{}',".format(dato[0], dato[1])
            sql = sql[:-1]
        
        logging.info('Realizando SELECT: '+sql)
        
        try:
            self.cursor.execute(sql)
            datos = self.cursor.fetchall()
            return datos
        
        except pymysql.err.OperationalError as e:
            logging.warning("Error De Operacion: " + str(e))
            return 1
        
        except pymysql.err.IntegrityError as e:
            logging.warning("Error de Integridad: " + str(e))
            return 2
    
    def update(self, tabla: str, *args, **kwargs) -> int:
        sql = 'UPDATE {} SET '.format(tabla)
        
        i = 0
        for dato in args:
            if i%2 == 0:
                sql += '{}='.format(dato)
            else:
                sql += r"'{}',".format(dato)
            i += 1
        sql = sql[:-1]
        
        if len(kwargs) != 0:
            cont = 0
            for dato in kwargs.items():
                if cont == 0:
                    sql += ' WHERE '
                else:
                    sql = sql[:-1]
                    sql += ' AND '
                cont += 1
                
                sql += r"{}='{}',".format(dato[0], dato[1])
            sql = sql[:-1] + ' LIMIT 1'
        
        logging.info('Realizando UPDATE: '+sql)
        
        try:
            self.cursor.execute(sql)
        
        except pymysql.err.OperationalError as e:
            logging.warning("Error De Operacion: " + str(e))
            return 1
        except pymysql.err.IntegrityError as e:
            logging.info("Error de Integridad: " + str(e))
            return 2
        
        return 0

def insert_song(nombre: str, interprete: str) -> int | None:
    db = DataBase()
    res = db.insert('songs', song_name=nombre, interprete=interprete)
    match res:
        case 0:
            db.connection.commit()
            return db.select('songs', 'song_id', song_name=nombre, interprete=interprete)[0][0]
        case 1:
            print('Error de Operacion')
            return None
        case 2:
            print('Error de Integridad')
            return None

def insert_hashes(id_song: int, hashes: list[tuple[str, int]]) -> int:
    db = DataBase()
    
    sql = 'INSERT INTO fingerprints(song_id, hash, offset) VALUES '
    
    for hash in hashes:
        sql += "({}, '{}', {}),".format(id_song, hash[0], hash[1])
    
    sql = sql[:-1]
    logging.warning("SQL Fingerpints: " + sql)
    
    try:
        db.cursor.execute(sql)
    
    except pymysql.err.OperationalError as e:
        logging.warning("Error De Operacion: " + str(e))
        print('Error de Operacion')
        return 1
    
    except pymysql.err.IntegrityError as e:
        logging.info("Error de Integridad: " + str(e))
        print('Error de Integridad')
        return 2
    
    db.update('songs', 'fingerprinted', 1, song_id=id_song)
    db.connection.commit()
    
    return 0

def return_matches(hashes: list[tuple[str, int]]) ->  tuple[list[tuple[int, int]], dict[int, int]]:
    db = DataBase()
    """Searches the database for a song match given a list of hashes in pairs of (hash, offset)
    returns a of (sid, offset_difference) tuples and a dictionary with the amount of hashes matched (not considering
        duplicated hashes) in each song.
            - song id: Song identifier
            - offset_difference: (database_offset - sampled_offset)"""

            # Create a dictionary of hashes and their offsets
    mapper = {}
    # Get the hashes from the mapper
    for hsh, offset in hashes:
        if hsh.upper() in mapper.keys():
            mapper[hsh.upper()].append(offset)
        else:
            mapper[hsh.upper()] = [offset]
    
    values = list(mapper.keys())

    #Count the number of hashes in the query without duplicates
    query_hash_count = dict()
    results = []
    #with db.cursor() as cursor
    for index in range(len(values),1000):
        # create query
        sql = 'SELECT song_id, hash, offset FROM fingerprints WHERE hash IN ({})'.format(','.join(['%s'] * len(values[index-1000:index])))
        
        # execute query

        db.cursor.execute(sql, values[index-1000:index])
        resultset = db.cursor.fetchall()

        for song_id,hsh,offset in resultset:
            if song_id in query_hash_count:
                query_hash_count[song_id] += 1
            else:
                query_hash_count[song_id] = 1

            # Calculate the offset difference
            offset_difference = offset - mapper.get(hsh.upper())[0]
            results.append((song_id, offset_difference))
        
    return results, query_hash_count


def get_song_by_id(song_id: int) -> tuple[str, str] | None:
    db = DataBase()
    res = db.select('songs', 'song_name', 'interprete', song_id=song_id)
    if res == 1:
        print('Error de Operacion')
        return None
    elif res == 2:
        print('Error de Integridad')
        return None
    else:
        return res[0]
