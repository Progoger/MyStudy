GET_LESSONS = """
    select "ID" "id", "Name" "title" from "Lesson" where "DirectionID" = %s
"""

ADD_LESSON = """
    insert into "Lesson" values (%s, %s, %s)
    returning "ID" "id", "Name" "title"
"""

DELETE_LESSON = """
    delete from "Lesson"
    where "ID" = %s
"""

EDIT_LESSON = """
    update "Lesson" set "Name" = %s where "ID" = %s
    returning "ID" "id", "Name" "title" 
"""

ADD_LESSON_TYPE = """
    insert into "LessonType" values(%s, %s, %s)
    returning "ID" "type", "Type" "name", "LogoType" "logoType"
"""

GET_LESSON_TYPES = """
    select 
        "ID" "type"
    ,   "Type" "name"
    ,   "LogoType" "logoType"
    from "LessonType"
"""

EDIT_LESSON_TYPE = """
    update "LessonType"
    set
        "Type" = %s
    ,   "LogoType" = %s
    where
        "ID" = %s
"""

DELETE_LESSON_TYPE = """
    delete from "LessonType"
    where "ID" = %s
"""