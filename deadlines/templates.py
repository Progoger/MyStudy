CREATE_DEADLINE = """
    insert into "Deadline" values(%s, %s, %s, %s, %s)
    returning "ID" "id"
"""

ADD_USER_TO_DEADLINE = """
    insert into "Deadlines/Users" values(%s, %s)
"""

GET_DEADLINES = """
    select 
        "ID" "id"
    ,   "Text" "text"
    ,   "DateEnd" "end"
    ,   "LessonID" "lessonId"
    ,   "UserID"    "userId"
    from "Deadline" d 
    inner join "Deadlines/Users" du on du."UserID" = %s
"""