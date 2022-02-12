from json.tool import main
import metallum
from collections import deque
import json


def main():
    MAX_DEPTH = 1
    SCORE_THRESHOLD = 30


    visitedBands = [metallum.band_for_id(4237), metallum.band_for_id(91),  metallum.band_for_id(4861)]
    visitedBandsIds = set()
    queued_bands = deque()

    #add root bands
    for band in visitedBands:
        visitedBandsIds.add(band.id)
        queued_bands.append(band)


    depth = 0

    #BFS exploring of similar artists of root bands
    while depth < MAX_DEPTH:
        exploring = queued_bands
        queued_bands = deque()
        while not len(exploring) == 0:
            band : metallum.Band = exploring.pop()
            band_sa : metallum.SimilarArtistsResult = band.similar_artists
            band_sa = [band for band in band_sa if band.id not in visitedBandsIds and band.score >= SCORE_THRESHOLD]
            counter = len(band_sa)
            for sa in band_sa:
                print("sim artist left:", counter)
                sa : metallum.Band = sa.get()
                queued_bands.append(sa)
                visitedBandsIds.add(sa.id)
                visitedBands.append(sa)
                counter-=1
        depth +=1



    visitedBandsJSON = []
    left = len(visitedBands)
    #make objects for json
    for visitedBand in visitedBands:
        print(left)
        
        band_obj = visitedBand.to_object
        sim_art_list = band_obj["sim_artists"]
        sim_art_list = list(filter(lambda a: a["id"] in visitedBandsIds, sim_art_list))
        band_obj["sim_artists"] = sim_art_list

        visitedBandsJSON.append(band_obj)
        left-=1


    with open('json_data_test.json', 'w') as file:
        json.dump(visitedBandsJSON, file)


if __name__ == "__main__":
    main()