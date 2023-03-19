import json
import time as banana

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal

start_time = banana.time()
lastroom = None
cache = None
pages = list(extract_pages("classdata.pdf", page_numbers=[0],caching=True))


def getCoords(element):
    for p in pages:
        for e in p:
            if isinstance(e, LTTextBoxHorizontal):
                if e.get_text() == element:
                    l = (e.x0, e.y0)
                    return l



def getPageCache(room):
    global lastroom
    global cache

    if lastroom == room:
        lastroom = room
        return cache
    else:
        lastroom = room
        cache = list(extract_pages("classdata.pdf", page_numbers=[room],caching=True))
        return cache




def getRoomInfo(day, time, page):
    day = getCoords(f"{day}\n")[1]
    time = getCoords(f"{time}\n")[0]



    desc = []

    for p in page:
        for e in p:
            if isinstance(e, LTTextBoxHorizontal):
                if day - 20 <= e.y0 <= day + 20 and time - 5 <= e.x0 <= time + 5:
                    desc.append(e.get_text())

    return desc


def getDays():
    return ["Mo", "Di", "Mi", "Do", "Fr"]


def getTimes():
    return ["8:00", "8:55", "9:50", "10:50", "11:45", "12:35", "13:25", "14:20", "15:15", "16:10", "17:00"]


def getRooms():
    return ["G1a", "G1b", "G1c", "G1d", "G1e", "G1f", "G2a", "G2b", "G2c", "G2d", "G2e", "G3a", "G3b", "G3c", "G3e",
            "G4a", "G4b", "G4c", "G4d", "G4e", "W1a",
            "W1b", "W1c", "W1d", "W2a", "W2b", "W2c", "W2d", "W3a", "W3b", "W3c", "I1a", "I1b", "I2a", "I2b", "I3a",
            "I3b"]


def buildJson(file_path):
    d = {"data": {}}
    counter = 0
    days = getDays()
    times = getTimes()
    rooms = getRooms()
    for r in rooms:
        if counter == 1:
            print(f"estimated time: {(banana.time() - start_time)} seconds")
        print(f"started {counter + 1}/{len(rooms)} after {banana.time() - start_time}s")
        counter += 1
        d["data"][r] = {}
        for dy in days:
            d["data"][r][dy] = {}
            for t in times:
                d["data"][r][dy][t] = getRoomInfo(dy, t, getPageCache(rooms.index(r)))

    with open(file_path, "w") as f:
        json.dump(d, f)


buildJson("class.json")

print(f"Building the Json took: {banana.time() - start_time} seconds")
