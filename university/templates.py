GET_ALL_INSTITUTES = """
    select "ID" "id", "Name" "title" from "Institute"
    WHERE "OrganisationID" = %s
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