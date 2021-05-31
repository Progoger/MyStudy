GET_ALL_INSTITUTES = """
    select "ID" "id", "Name" "title" from "Institute"
"""

GET_DIRECTIONS = """
    select "ID" "id", "Name" "title" from "Direction" where "InstituteID" = %s 
"""

ADD_DIRECTION = """
    insert into "Direction" values (%s, %s, %s)
    returning "ID" "id", "Name" "title"
"""

ADD_INSTITUTE = """
    insert into "Institute" values (%s, %s)
    returning "ID" "id", "Name" "title"
"""

DEL_INSTITUTE = """
    delete from "Institute" where "ID" = %s
    returning "ID" "id", "Name" "title"
"""

DEL_DIRECTION = """
    delete from "Direction" where "ID" = %s
    returning "ID" "id", "Name" "title"
"""

EDIT_DIRECTION = """
    update "Direction" set "Title" = %s where "ID" = %s
    returning "ID" "id", "Name" "title"
"""

EDIT_INSTITUTE = """
    update "Institute" set "Title" = %s where "ID" = %s
    returning "ID" "id", "Name" "title"
"""