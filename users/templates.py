GET_DATA_BY_LOGIN = """
SELECT "Password",
       "Session",
       "EducationalID"::text AS "Schema",
       E."Color",
       E."Name" AS "University" 
FROM "Authorization"
INNER JOIN "Educational" E on E."Schema" = "EducationalID" 
WHERE "Login" = %s
"""

UPDATE_SESSION_BY_LOGIN = """
UPDATE "Authorization" SET "Session" = %s,
                           "DateActivity" = %s 
WHERE "Login" = %s
"""

GET_USER_DATA_BY_SESSION = """
SELECT 
    "Login",
    "Session",
    "EducationalID"::text AS "Schema", 
    E."Color",
    E."Name" AS "University" 
FROM "Authorization"
INNER JOIN "Educational" E on E."Schema" = "Authorization"."EducationalID"
WHERE "Session" = %s
"""

GET_TEACHERS = """
    select u."ID", u."Name", u."Surname", u."Patronymic" from "Teachers" t 
    join "User" u on u."ID" = t."UserID"
    where t."LessonID" = %s
"""

GET_TEACHERS_BY_INSTITUTE = """
    select 
	u."ID" "id"
,	u."Name" "name"
,	u."Surname" "surname"
,	u."Patronymic" "patronymic"
from "User" u
inner join 
	"Direction" d 
on u."DirectionID" = d."ID" 
where d."InstituteID" = %s and u."Group" is NULL
"""

INSERT_TEACHER = """
    insert into "User" ("ID", "Name", "Surname", "Patronymic", "DirectionID")
    values(%s, %s, %s, %s, %s)
"""