from Audio_Fingerprinting import *
import Fingerprint_alignment as fa
from MySQLDB import *
from scipy.io import wavfile
#LOGGING CONFIG
logging.basicConfig(filename='log_basedatos.log', encoding='utf-8', level=logging.DEBUG)
#MAIN

#user input
#archivo = 'Lavender_Town_Japan.wav'
#samplerate,data = wavfile.read(archivo)
# nombre = input("Ingresa el nombre de la cancion: ")
#interprete = input("Ingresa el nombre del autor: ")

#insert song into database
#hashes = fingerprint(data)
#id = insert_song(nombre, interprete)
#print(id)

#if id is not None:
    #insert_hashes(id, hashes)

#insert song into database
def songs_toDB():
    #insert  gorillaz song
    file='input_songs/Baby Queen slowed.wav'
    samplerate,data = wavfile.read(file)
    nombre = "Baby Queen"
    interprete = "Gorillaz"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)
    
    #insert  Skrillex song

    file='input_songs/Bangarang.wav'
    samplerate,data = wavfile.read(file)
    nombre = "Bangarang"
    interprete = "Skrillex"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)

    #insert Despacito song
    file='input_songs/Despacito.wav'
    samplerate,data = wavfile.read(file)
    nombre = "Despacito"
    interprete = "Luis Fonsi"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)
    
    #insert Disc 13 song
    file='input_songs/Disc 13.wav'
    samplerate,data = wavfile.read(file)
    nombre = "Disc 13"
    interprete = "C418"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)
    
    #insert disc 11 song
    file='input_songs/Disc 11.wav'
    samplerate,data = wavfile.read(file)
    nombre = "Disc 11"
    interprete = "C418"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes) 

    #insert Clams Casino song
    file = "input_songs/I'm God.wav"
    samplerate,data = wavfile.read(file)
    nombre = "Im God"
    interprete = "Clams Casino"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)
    
    #insert Monster song
    file = "input_songs/Monster.wav"
    samplerate,data = wavfile.read(file)
    nombre = "Monster"
    interprete = "Meg & Dia"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)
    
    # insert Martin Garrix song
    file = "input_songs/These Are The Times.wav"
    samplerate,data = wavfile.read(file)
    nombre = "These Are The Times"
    interprete = "Martin Garrix"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)
        
    #insert virtual self Ghost Voices song
    file = "input_songs/Ghost Voices.wav"
    samplerate,data = wavfile.read(file)
    nombre = "Ghost Voices"
    interprete = "Virtual Self"
    hashes = fingerprint(data)
    id = insert_song(nombre, interprete)
    print(id)
    if id is not None:
        insert_hashes(id, hashes)

#songs_toDB()

#input recording to compare
file = "split.wav"
samplerate,data = wavfile.read(file)
#fingerprinting input recording unpacking
hashes , process_time = fa.genFingerprints(data, samplerate)
print("Fingerprinting time: ", process_time, " seconds")
#compare fingerprints with database
matches, query_matches, processing_Time = fa.findMatches(hashes)
print("Processing comparing time: ", processing_Time, " seconds")
#align matches
match_results = fa.align_matches(matches, query_matches,2)

#display results
#print("Results:", match_results)
print("Results:")
for result in match_results:
    print("Song: ", result.get("song_name"), " by ", result.get("song_author"), " with ", result.get("hashes_matched"), " matches")


