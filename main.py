from Audio_Fingerprinting import fingerprint
from MySQLDB import *
from scipy.io import wavfile
#LOGGING CONFIG
logging.basicConfig(filename='log_basedatos.log', encoding='utf-8', level=logging.DEBUG)
#MAIN
#user input
archivo = 'Lavender_Town_Japan.wav'
samplerate,data = wavfile.read(archivo)
nombre = input("Ingresa el nombre de la cancion: ")
interprete = input("Ingresa el nombre del autor: ")

#insert song into database
hashes = fingerprint(data)
id = insert_song(nombre, interprete)
print(id)

if id is not None:
    insert_hashes(id, hashes)

#fingerprint alignment

