GET_LESSONS = """
    select "ID" "id", "Name" "title" from "Lesson" where "DirectionID" = %s
"""

ADD_LESSON = """
    insert into "Lesson" values (%s, %s, %s)
    returning "ID" "id", "Name" "title"
"""

DELETE_SCHEDULE_GROUP_BY_LESSON = """
    delete from "Schedule/Group"
    where "ScheduleId" in (
        select "ID" from "Schedule"
        where "LessonID" = %s
    )
"""

DELETE_SCHEDULES_BY_LESSON = """
    delete from "Schedule"
    where "LessonID" = %s
"""

DELETE_TEACHERS_LESSON = """
    delete from "Teachers"
    where "LessonID" = %s
"""

DELETE_LESSON = """
    delete from "Lesson"
    where "ID" = %s
"""