ADD_SCHEDULE = """
    insert into "Schedule" values(%s::uuid, %s::uuid, %s::int4, %s::int4, %s::int4, %s::uuid, %s::uuid, %s::int4, %s, %s::time, %s::time)
    returning "ID" "id"
"""

ADD_GROUP_TO_SCHEDULE = """
    insert into "Schedule/Group" values(%s, %s)
"""

GET_SCHEDULE = """
    select
        "ID" "id"
    ,   "DayOfWeek" "weekday"
    ,	"PairNumber" "time"
    ,	"NumberOfWeek" "week"
    ,	lt."Type" "typename"
    ,	"LessonType" "type"
    ,	l."Name" "lessonTitle"
    ,	"TeacherId" "tutorid"
    ,	u."Name" "name"
    ,	u."Surname" "surname"
    ,	u."Patronymic" "patronymic"
    ,	h."ID" "addressid"
    ,	h."Address" "address"
    ,	"AudienceNumber" "classid"
    ,	"GroupId" "group"
    ,   "StartTime" "start"
    ,   "EndTime" "end"
    from(
        SELECT * from "Schedule" s 
    inner join (
        select 
            sg."ScheduleId"
        ,	case 
                when cou = 1 then sg."GroupId"
                else %s
            end "GroupId"
        from "Schedule/Group" sg
        inner join (
            select 
                "ScheduleId"
            ,	COUNT("GroupId") cou 
            from "Schedule/Group"  
            where "GroupId" like %s
            group by "ScheduleId"
        ) sg2 
        on sg."ScheduleId" = sg2."ScheduleId"
    ) sg
    on s."ID" = sg."ScheduleId"
    ) ssg
    inner join "Lesson" l on ssg."LessonID" = l."ID"
    inner join "LessonType" lt on ssg."LessonType" = lt."ID"
    inner join "User" u on ssg."TeacherId" = u."ID"
    inner join "Housing" h on ssg."HousingID" = h."ID" 
"""

GET_SCHEDULE_BY_DAY = """
    select
        "ID" "id"
    ,   "DayOfWeek" "weekday"
    ,	"PairNumber" "time"
    ,	"NumberOfWeek" "week"
    ,	lt."Type" "typename"
    ,	"LessonType" "type"
    ,	l."Name" "lessonTitle"
    ,	"TeacherId" "tutorid"
    ,	u."Name" "name"
    ,	u."Surname" "surname"
    ,	u."Patronymic" "patronymic"
    ,	h."ID" "addressid"
    ,	h."Address" "address"
    ,	"AudienceNumber" "classid"
    ,	"GroupId" "group"
    ,   "StartTime" "start"
    ,   "EndTime" "end"
    from(
        SELECT * from "Schedule" s 
        inner join "Schedule/Group" sg on  s."ID" = sg."ScheduleId"
        where "GroupId" = %s
    ) ssg
    inner join "Lesson" l on ssg."LessonID" = l."ID"
    inner join "LessonType" lt on ssg."LessonType" = lt."ID"
    inner join "User" u on ssg."TeacherId" = u."ID"
    inner join "Housing" h on ssg."HousingID" = h."ID" 
    where "DayOfWeek" = %s and "NumberOfWeek" = %s
    order by "PairNumber" 
"""

DELETE_EVENT_WITH_GROUPS = """
    delete from "Schedule/Group"
    where "ScheduleId" = %s
"""

DELETE_EVENT = """
    delete from "Schedule"
    where "ID" = %s
"""