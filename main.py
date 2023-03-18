import json
import time as banana

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal

start_time = banana.time()

pages = list(extract_pages("data1.pdf", page_numbers=[0]))


def getCoords(element):
    for p in pages:
        for e in p:
            if isinstance(e, LTTextBoxHorizontal):
                if e.get_text() == element:
                    l = (e.x0, e.y0)
                    return l


def getRoomInfo(day, time, room):
    day = getCoords(f"{day}\n")[1]
    time = getCoords(f"{time}\n")[0]
    desc = []
    for p in extract_pages("data1.pdf", page_numbers=[room]):
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
    return ['Th1', 'Th2', 'Th3', 'Th4', 'Th5', '10', '11', '12', '105', '106', '107', '108', '110', '113', '114', '117',
            '118', '120', '121', '123', '124', '204', '205', '206', '207', '211', '215', '220', '221', '222', '223',
            '224', '226', '227', "311", "313", "318", "319", "320", "321", "322", "324", "325", '411', '412', '413',
            '415', '418', '419', '421', '422', '423', '424', '425']


def roomnametoint(room):
    return getRooms().index(room)


def buildJson(file_path):
    d = {"data": {}}
    counter = 0
    for r in getRooms():
        if counter == 1:
            print(f"Estimated time: {(banana.time() - start_time) * len(getRooms()) / 60} minutes")
        print(f"file parsed {counter}/{len(getRooms())} after {banana.time() - start_time} seconds")
        counter += 1
        d["data"][r] = {}
        for dy in getDays():
            d["data"][r][dy] = {}
            for t in getTimes():
                d["data"][r][dy][t] = getRoomInfo(dy, t, roomnametoint(r))

    with open(file_path, "w") as f:
        json.dump(d, f)


buildJson("out.json")
print(f"Building the Json took: {banana.time() - start_time} seconds")
