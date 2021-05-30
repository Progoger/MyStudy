from uuid import uuid4
from generals.database import Database
from schedule.templates import ADD_SCHEDULE, ADD_GROUP_TO_SCHEDULE
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

DaysOfWeek = {
    'Понедельник':1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6,
    'Воскресенье': 7
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
