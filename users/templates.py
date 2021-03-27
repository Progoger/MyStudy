GET_PASSWORD_BY_LOGIN = """
SELECT "Password", "Session", "EducationalID"::text "Schema" FROM "Authorization" WHERE "Login" = %s
"""

UPDATE_SESSION_BY_LOGIN = """
UPDATE "Authorization" SET "Session" = %s,
                           "DateActivity" = %s 
WHERE "Login" = %s
"""
