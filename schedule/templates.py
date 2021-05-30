ADD_SCHEDULE = """
    insert into "Schedule" values(%s::uuid, %s::uuid, %s::int4, %s::int4, %s::int4, %s::uuid, %s::uuid, %s::int4, %s)
    returning "ID" "id"
"""

ADD_GROUP_TO_SCHEDULE = """
    insert into "Schedule/Group" values(%s, %s)
"""