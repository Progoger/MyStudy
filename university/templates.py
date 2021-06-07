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
    update "Direction" set "Name" = %s where "ID" = %s
    returning "ID" "id", "Name" "title"
"""

EDIT_INSTITUTE = """
    update "Institute" set "Name" = %s where "ID" = %s
    returning "ID" "id", "Name" "title"
"""

GET_DIRECTIONS_WITH_GROUPS = """
    select
        "ID" "directionId"
    ,	d."Name" "direction"
    ,	g."Name" "subgroup"
    ,	g."ParentGroup" "group"
    from "Direction" d
    inner join "Group" g on d."ID" = g."DirectionId" 
    where "InstituteID" = %s
    order by "direction", "group"
"""