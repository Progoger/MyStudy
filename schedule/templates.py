ADD_SCHEDULE = """
    insert into "Schedule" values(%s::uuid, %s::uuid, %s::int4, %s::int4, %s::int4, %s::uuid, %s::uuid, %s::int4, %s)
    returning "ID" "id"
"""

ADD_GROUP_TO_SCHEDULE = """
    insert into "Schedule/Group" values(%s, %s)
"""

GET_SCHEDULE = """
    select 
        "DayOfWeek" "weekday"
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