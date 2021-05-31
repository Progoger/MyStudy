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

GET_GROUPS_BY_PARENTGROUP = """
    select "Name" "id" from "Group"
    where "ParentGroup" = %s
"""

CHECK_GROUP_EXIST = """
    select true from "Group"
    where "Name" = %s or "ParentName" = %s
"""

CHECK_SUBGROUP_GROUP = """
    select true from "Group"
    where "Name" = %s
"""

ADD_GROUP = """
    insert into "Group" values(%s, %s, %s, %s)
"""

UPDATE_GROUP_TO_SUBGROUP = """
    update "Group" set
        "ParentGroup" = "Name"
    ,   "Name" = %s
    ,   "Type" = %s
"""

EDIT_GROUP = """
    update "Group" set "Name" = %s, "ParentGroup" = %s, "Type" = %s where "Name" = %s 
"""