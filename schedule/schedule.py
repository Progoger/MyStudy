from uuid import uuid4
from generals.database import Database
from schedule.templates import DELETE_EVENT_WITH_GROUPS, DELETE_EVENT, ADD_SCHEDULE, ADD_GROUP_TO_SCHEDULE, GET_SCHEDULE, GET_SCHEDULE_BY_DAY
from groups.templates import GET_GROUPS_BY_PARENTGROUP
import json

pairNumbers = {
    '08:30 - 10:00': 1,
    '10:10 - 11:40': 2,
    '11:50 - 13:20': 3,
    '14:00 - 15:30': 4,
    '15:40 - 17:10': 5,
    '17:20 - 18:50': 6,
    '19:00 - 20:30': 7
    }

pairTime = {
    1: '8:30 - 10:00',
    2: '10:10 - 11:40',
    3: '11:50 - 13:20',
    4: '14:00 - 15:30',
    5: '15:40 - 17:10',
    6: '17:20 - 18:50',
    7: '19:00 - 20:30'
    }

DaysOfWeek = {
    'Понедельник':1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6,
    'Воскресенье': 7
    }

DaysOfWeek2 = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье'
    }


def add_schedule(params):
    db = Database(params['schema'])
    deleted_events = params.get('deletedEvents')
    if deleted_events:
        delete_events(db, deleted_events)
    dayList = params['dayList']
    for day in dayList:
        tup = {'DayOfWeek': day['cardTitle'], 'NumberOfWeek': day['week']}
        eventList = day['eventList']
        for i in range(len(eventList)):
            tup2 = {}
            tup2['LessonType'] = eventList[i]['type']
            event = eventList[i]['details']
            tup2['AudienceNumber'] = event['class']['id']
            tup2['HousingID'] = event['address']['id']
            tup2['LessonID'] = event['lesson']['id']
            tup2['TeacherID'] = event['tutor']['id']
            tup2['PairNumber'] = pairNumbers.get(event['time']['start']+' - '+event['time']['end'])
            tup2['StartTime'] = event['time']['start']
            tup2['EndTime'] = event['time']['end']
            schedule = db.SqlQueryRecord(
                ADD_SCHEDULE,
                uuid4(),
                tup2['LessonID'],
                DaysOfWeek[tup['DayOfWeek']],
                tup2['PairNumber'],
                tup['NumberOfWeek'],
                tup2['LessonType'],
                tup2['TeacherID'],
                tup2['AudienceNumber'],
                tup2['HousingID'],
                tup2['StartTime'],
                tup2['EndTime']
            )
            groups = event['groups']
            if not groups['subgroup']:
                for group in groups['groups']:
                    subgroups = db.SqlQuery(GET_GROUPS_BY_PARENTGROUP, group['id'])
                    for subgroup in subgroups:
                        db.SqlQuery(ADD_GROUP_TO_SCHEDULE, schedule['id'], subgroup['id'])
            else:
                db.SqlQuery(ADD_GROUP_TO_SCHEDULE, schedule['id'], groups['subgroup'][0]['id'])


def create_event(id, elem):
    event = {}
    event['id'] = elem['id']
    event['name'] = elem['typename']
    event['type'] = elem['type']
    details = {}
    details['lessonTitle'] = elem['lessonTitle']
    details['tutor'] = {
        'id': elem['tutorid'],
        'name': elem['name'],
        'surname': elem['surname'],
        'patronymic': elem['patronymic']
    }
    details['address'] = {
        'id': elem['addressid'],
        'address': elem['address']
    }
    details['time'] = {
        "start": elem['start'],
        "end": elem['end']
    }
    details['groups'] = {
        'groups': [
            {
                'title': id[:-1],
                'id': id[:-1]
            }
        ],
        'subgroup': [
            {
                'id': id
            }
        ]
    }
    event['details'] = details
    return event


def get_schedule(params):
    db = Database(params['schema'])
    query_res = db.SqlQuery(GET_SCHEDULE, params['id'], params['id'] + '%')
    dayList_dict = {'Понедельник_1': [],
                    'Вторник_1': [],
                    'Среда_1': [],
                    'Четверг_1': [],
                    'Пятница_1': [],
                    'Суббота_1': [],
                    'Понедельник_2': [],
                    'Вторник_2': [],
                    'Среда_2': [],
                    'Четверг_2': [],
                    'Пятница_2': [],
                    'Суббота_2': []
                    }
    for elem in query_res:
        event = {}
        event['loaded'] = True
        event['id'] = str(elem['id'])
        event['name'] = elem['typename']
        event['type'] = elem['type']
        event['logoType'] = elem['logoType']
        details = {}
        details['lesson'] = {
            'title': elem['lessonTitle'],
            'id': elem['lessonId']
        }
        details['tutor'] = {
            'id': elem['tutorid'],
            'name': elem['name'],
            'surname': elem['surname'],
            'patronymic': elem['patronymic']
        }
        details['class'] = {
            'id': elem['classid']
        }
        details['address'] = {
            'id': elem['addressid'],
            'address': elem['address']
        }
        details['time'] = {
            "start": str(elem['start'])[0:5],
            "end": str(elem['end'])[0:5]
        }
        subgroup = []
        if elem['group'] != params['id']:
            subgroup = [
                {
                    'id': elem['group']
                }
            ]

        details['groups'] = {
            'groups': [
                {
                    'title': elem['group'],
                    'id': elem['group']
                }
            ],
            'subgroup': subgroup
        }
        event['details'] = details
        dayList_dict[DaysOfWeek2[elem['weekday']] + '_' + str(elem['week'])].append(event)
    res_day_List = []
    for key, elem in dayList_dict.items():
        if elem:
            cardTitle, week = key.split('_')
            tmp = {}
            tmp['cardTitle'] = cardTitle
            tmp['week'] = week
            tmp['eventList'] = elem
            res_day_List.append(tmp)
    return res_day_List


def get_schedule_by_day(params):
    db = Database(params['schema'])
    query_res = db.SqlQuery(GET_SCHEDULE_BY_DAY, params['id'], params['day'], params['week'])
    event_list = []
    for elem in query_res:
        event = create_event(params['id'], elem)
        event_list.append(event)
    res = {}
    res['cardTitle'] = params['day']
    res['week'] = params['week']
    res['eventList'] = event_list
    return res


def delete_events(db, deleted_events):
    for event in deleted_events:
        db.SqlQuery(DELETE_EVENT_WITH_GROUPS, event['id'])
        db.SqlQuery(DELETE_EVENT, event['id'])
