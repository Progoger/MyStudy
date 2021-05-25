GET_LESSONS = """
    select "ID", "Name" from "Lesson" where "DirectionID" = %s
"""

ADD_LESSON = """
    insert into "Lesson" values (%s, %s, %s)
"""