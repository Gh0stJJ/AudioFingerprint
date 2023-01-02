
from mysqlDB import *
import os 
import sys 
from time import time
from itertools import groupby
import Audio_Fingerprinting as af

def genFingerprints(sdata: list[tuple[str, int]],sample_rate) -> tuple[list[tuple[str, int]] , dict[int, int], float]:
    
    t=time()
    hashes = af.fingerprint(sdata)
    fpTime= time()-t
    return hashes, fpTime

def findMatches(hases: list[tuple[str, int]]) -> tuple[list[tuple[int, int]], dict[str, int], float]:

    t=time()
    matches, query_matches = return_matches(hases)
    matchTime= time()-t
    return matches, query_matches, matchTime

# Find hash matches that aling in time with other hash matches and fit the time offset criteria
def align_matches(matches: list[tuple[int, int]], query_matches: dict[int, int], queried_hases: int) -> list[tuple[int, int, int]]:

    #count offset occurences
    sorted_matches = sorted(matches, key=lambda x: (x[0], x[1]))
    counts =[(*key, len(list(group))) for key, group in groupby(sorted_matches, key=lambda x: (x[0], x[1]))]
    songs_matches = sorted([max(list(group), key=lambda x: x[2]) for key, group in groupby(counts, key=lambda x: x[0])], key=lambda x: x[2], reverse=True)

    #Find songs resultset
    songs_resultset = []
    for song_id, offset, count in songs_matches[0:queried_hases]:
        song= get_song_by_id(song_id)

        #song name
        song_name = song[0]
        #song author
        song_author = song[1]
        nseconds = round((queried_hases - count) / queried_hases, 2)
        hashes_matched = query_matches[song_id]

        #dictionary with the song data
        song={ 'song_id': song_id, 'song_name': song_name, 'song_author': song_author, 'nseconds': nseconds, 'hashes_matched': hashes_matched}
        songs_resultset.append(song)


    return songs_resultset

