GET_ALL_GROUPS = """
    select "Name" "title" FROM "Group"
"""

GET_GROUPS_BY_DIRECTION = """
    select distinct("title"), "hasSubgroup"
    from(
        select 
            case
                when "ParentGroup" is null then "Name"
                else "ParentGroup"
            end "title"
        ,    case
                when "ParentGroup" is null then False
                else True
            end "hasSubgroup"
        from
        "Group"
        where "DirectionId" = %s
    ) res
"""

GET_GROUPS_BY_INSTITUTE_YEAR = """
    select distinct("title")
    from(
        select 
            case
                when "ParentGroup" is null then g."Name"
                else "ParentGroup"
            end "title"
        from
        "Group" g
        inner join "Direction" d on d."InstituteID" = %s
    ) res
    where "title" like %s
"""

GET_GROUPS_BY_PARENTGROUP = """
    select "Name" "id" from "Group"
    where "ParentGroup" = %s
"""

CHECK_GROUP_EXIST = """
    select true from "Group"
    where "Name" = %s or "ParentGroup" = %s
"""

CHECK_SUBGROUP_GROUP = """
    select true from "Group"
    where "Name" = %s
"""

ADD_GROUP = """
    insert into "Group" values(%s, %s, %s, %s)
    returning "Name" "id"
"""

UPDATE_GROUP_TO_SUBGROUP = """
    update "Group" set
        "ParentGroup" = "Name"
    ,   "Name" = %s
    ,   "Type" = %s
    where "Name" = %s
    returning "Name" "id"
"""

DELETE_SCHEDULE_GROUP = """
    delete from "Schedule/Group"
    where "GroupId" = %s
"""

DELETE_GROUP = """
    delete from "Group"
    where "ParentGroup" = %s
"""

DELETE_SUBGROUP = """
    delete from "Group"
    where "Name" = %s
"""