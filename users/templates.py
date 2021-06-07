GET_DATA_BY_LOGIN = """
SELECT "Password",
       "Session",
       "EducationalID"::text AS "Schema",
       E."Color",
       E."Name" AS "University",
       "Role"::text
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
    E."Name" AS "University",
    "Role"::text
FROM "Authorization"
INNER JOIN "Educational" E on E."Schema" = "Authorization"."EducationalID"
WHERE "Session" = %s
"""

GET_TEACHERS = """
    select u."ID" "id", u."Name" "name", u."Surname" "surname", u."Patronymic" "patronymic" from "Teachers" t 
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
where d."InstituteID" = %s and u."IsTeacher" is True
"""

ADD_TEACHER = """
    insert into "User" ("ID", "Name", "Surname", "Patronymic", "DirectionID")
    values(%s, %s, %s, %s, %s)
    returning "ID" "id", "Name" "name", "Surname" "surname", "Patronymic" "patronymic"
"""

ADD_TEACHER_TO_LESSON = """
    insert into "Teachers"
    values (%s, %s)
"""

DELETE_TEACHERS_FROM_LESSON = """
    delete from "Teachers"
    where "LessonID" = %s
"""

ADD_SHEDULE = """
    insert into "Shedule" 
"""

CHECK_TEACHER_LESSON = """
    select true from "Teachers"
    where "LessonID" = %s
"""

UPDATE_STUDENT_GROUP_BY_CODE = """
update "User" set "Group" = (select "Group" from "InviteCodes" where "Code" = %s)
where "Login" = %s;

update "InviteCodes" set "IsActive" = false where "Code" = %s
"""

CHECK_USER_TO_USE_CODE = """
SELECT  EXISTS(select null from "User" where "Login" = login and "Group" is null) can_activate,
        EXISTS(select null FROM "Authorization" where "Login" = login) exists_global,
        EXISTS(select null from "InviteCodes" where "Code" = %s and "IsActive" is true) active_code
from (select %s as login) login
"""

CREATE_USER = """
INSERT INTO "Autorization" VALUES (%s, %s, null, null, true, %s);
INSERT INTO "User" VALUES (%s, %s, %s, %s, %s, (select "Group" from "InviteCodes" where "Code" = %s), (select j."DirectionID" from "InviteCodes" i where i."Code" = %s join "Group" j on j."Name" = i."Group"), false);
update "InviteCodes" set "IsActive" = false where "Code" = %s
"""

CHECK_LOGIN = """
select EXISTS(select null from "User" where "Login" = %s and "Group" is null) cannot_login
"""
