GET_ALL_UNIVERSITIES = """
select "ID", "Name" from "Institute"
"""

GET_ALL_DIRECTIONS = """
select "ID", "Name" from "Direction" where "InstituteID" = %s 
"""