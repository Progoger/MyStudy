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
