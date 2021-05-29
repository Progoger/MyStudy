GET_ALL_INSTITUTES = """
select "ID", "Name" from "Institute"
"""

GET_DIRECTIONS = """
select "ID", "Name" from "Direction" where "InstituteID" = %s 
"""

ADD_DIRECTION = """
    insert into "Direction" values (%s, %s, %s)
    returning *
"""

ADD_INSTITUTE = """
    insert into "Direction" values (%s, %s)
    returning *
"""