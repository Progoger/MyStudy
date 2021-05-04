from flask import Flask, request, jsonify, send_from_directory
import uuid
import copy


pairNumbers = {
    '8:30 - 10:00':1, 
    '10:10 - 11:40': 2, 
    '11:50 - 13:20': 3, 
    '14:00 - 15:30': 4, 
    '15:40 - 17:10': 5,
    '17:20 - 18:50': 6,
    '19:00 - 20:30': 7
    }


def parser(params):
    meta = copy.deepcopy(params['meta'])
    for key in meta:
        meta[key] = uuid.UUID(meta[key])
    
    dayList = copy.deepcopy(params['dayList'])
    res_dayList = []
    for tmp in dayList:
        tup = {'cardId':uuid.UUID(tmp['cardId']), 'cardTitle': tmp['cardTitle'], 'week': tmp['week']}
        eventList = copy.deepcopy(tmp['eventList'])
        res_eventList = []
        for event in eventList:
            tup2 = {}
            tup2['address'] = event['address']
            tup2['class'] = event['class']
            tup2['groups'] = copy.deepcopy(event['groups'])
            tup2['type'] = uuid.UUID(event['type'])
            tup2['lessonTitle'] = event['lessonTitle']
            tup2['tutor'] = event['tutor']
            tup2['PairNumber'] = pairNumbers[event['time']]
            res_eventList.append = tup2
        tup['eventList'] = res_eventList
        res_dayList.append(tup)
    return res_dayList

