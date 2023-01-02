import pymysql
import logging

class DataBase:
    __instance = None

    def __new__(cls):
        if DataBase.__instance is None:
            print('Nueva instancia')
            DataBase.__instance = object.__new__(cls)
        
        return DataBase.__instance

    def __init__(self):
        self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='admin',
                database='fingerprint'
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