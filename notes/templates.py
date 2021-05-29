GET_DATA_BY_ID = """
SELECT * FROM "TheNote"
WHERE "ID" = %s
"""

INSERT_DATA = """
INSERT INTO "TheNote" VALUES(%s, %s, %s, %s, %s)
"""

UPDATE_DATA_BY_ID = """
UPDATE "TheNote"
    SET "ID" = %s
,   SET "Date" = %s
,   SET "DateEnd" = %s
,   SET "Text" = %s
,   SET "AuthorId" = %s    
WHERE "ID" = %s
"""