GET_LESSONS = """
    select "ID" "id", "Name" "title" from "Lesson" where "DirectionID" = %s
"""

ADD_LESSON = """
    insert into "Lesson" values (%s, %s, %s)
    returning "ID" "id", "Name" "title"
"""