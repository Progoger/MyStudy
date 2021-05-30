GET_ALL_GROUPS = """
    select "Name" "title" FROM "Group"
"""

GET_GROUPS_BY_DIRECTION = """
select distinct("title")
from(
    select 
        case
            when "ParentGroup" is null then "Name"
            else "ParentGroup"
        end "title"
    from
    "Group"
    where "DirectionId" = %s
) res
"""


CHECK_SUBGROUP_GROUP = """
SELECT true FROM "Group"
WHERE "Name" = %s
"""

ADD_GROUP = """
    insert into "Group" values(%s, %s, %s, %s)
"""