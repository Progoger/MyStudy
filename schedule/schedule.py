from uuid import uuid4
from generals.database import Database
from schedule.templates import ADD_SCHEDULE, ADD_GROUP_TO_SCHEDULE, GET_SCHEDULE
from groups.templates import GET_GROUPS_BY_PARENTGROUP


pairNumbers = {
    '8:30 - 10:00':1,
    '10:10 - 11:40': 2,
    '11:50 - 13:20': 3,
    '14:00 - 15:30': 4,
    '15:40 - 17:10': 5,
    '17:20 - 18:50': 6,
    '19:00 - 20:30': 7
    }

pairTime = {
    1:'8:30 - 10:00',
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
            tup2['PairNumber'] = pairNumbers[event['time']]
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
                tup2['HousingID']
            )
            groups = event['groups']
            if groups['subgroup'] is None:
                for group in groups['groups']:
                    subgroups = db.SqlQuery(GET_GROUPS_BY_PARENTGROUP, group['id'])
                    for subgroup in subgroups:
                        db.SqlQuery(ADD_GROUP_TO_SCHEDULE, schedule['id'], subgroup['id'])
            else:
                db.SqlQuery(ADD_GROUP_TO_SCHEDULE, schedule['id'], groups['subgroup'][0]['id'])


def get_schedule(params):
    db = Database(params['schema'])
    query_res = db.SqlQuery(GET_SCHEDULE, params['id'], params['id']+'%')
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
        event['name'] = elem['typename']
        event['type'] = elem['type']
        details = {}
        details['lessonTitle'] = elem['lessonTitle']
        details['tutor'] ={
            'id': elem['tutorid'],
            'name': elem['name'],
            'surname': elem['surname'],
            'patronymic': elem['patronymic']
        }
        details['address'] = {
            'id': elem['addressid'],
            'address': elem['address']
        }
        details['time'] = pairTime[elem['time']]
        subgroup = None
        if elem['group'] != params['id']:
            subgroup = elem['group']
        details['groups'] = {
            'groups': [
                {
                    'title': params['id'],
                    'id': params['id']
                }
            ],
            'subgroup': [
                {
                    'id': subgroup
                }
            ]
        }
        event['details'] = details
        dayList_dict[DaysOfWeek2[elem['weekday']]+'_'+str(elem['week'])].append(event)
    res = []
    for key, elem in dayList_dict.items():
        if elem:
            cardTitle, week = key.split('_')
            tmp = {}
            tmp['cardTitle'] = cardTitle
            tmp['week'] = week
            tmp['eventList'] = elem
            res.append(tmp)
    return res
