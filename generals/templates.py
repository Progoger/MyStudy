# TODO: ПЕРЕД РЕГИСТРАЦИЕЙ НОВОГО АККАУНТА, НЕОБХОДИМО ОБНОВИТЬ К НОВОМУ ФОРМАТУ!!!
NEW_SCHEMA = """
CREATE SCHEMA %s
    AUTHORIZATION tatfezxgvgaefs;

set search_path = %s;
    
CREATE TABLE "LessonType"
(
    "ID" uuid NOT NULL,
    "Type" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "LessonType_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE "LessonType"
    OWNER to tatfezxgvgaefs;

CREATE TABLE "Housing"
(
    "ID" text COLLATE pg_catalog."default" NOT NULL,
    "Address" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Housing_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE "Housing"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Audience"
(
    "Number" text COLLATE pg_catalog."default" NOT NULL,
    "HousingID" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Audience_pkey" PRIMARY KEY ("Number"),
    CONSTRAINT "Audience_HousingID_fkey" FOREIGN KEY ("HousingID")
        REFERENCES "Housing" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "Audience"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Lesson"
(
    "ID" uuid NOT NULL,
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Lesson_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE "Lesson"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Institute"
(
    "ID" uuid NOT NULL,
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Institute_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE "Institute"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Direction"
(
    "ID" uuid NOT NULL,
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "InstituteID" uuid NOT NULL,
    CONSTRAINT "Direction_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "Direction_InstituteID_fkey" FOREIGN KEY ("InstituteID")
        REFERENCES "Institute" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "Direction"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Group"
(
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "ParentGroup" text COLLATE pg_catalog."default",
    CONSTRAINT "Group_pkey" PRIMARY KEY ("Name")
)

TABLESPACE pg_default;

ALTER TABLE "Group"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "User"
(
    "ID" uuid NOT NULL,
    "Login" text COLLATE pg_catalog."default",
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "Surname" text COLLATE pg_catalog."default" NOT NULL,
    "Patronymic" text COLLATE pg_catalog."default",
    "Group" text COLLATE pg_catalog."default",
    "DirectionID" uuid,
    CONSTRAINT "User_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "Direction_ID_fkey" FOREIGN KEY ("DirectionID")
        REFERENCES "Direction" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Group_Name_fkey" FOREIGN KEY ("Group")
        REFERENCES "Group" ("Name") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "User_Login_fkey" FOREIGN KEY ("Login")
        REFERENCES public."Authorization" ("Login") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "User"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "TheNote"
(
    "ID" uuid NOT NULL,
    "Date" timestamp without time zone NOT NULL,
    "DateEnd" timestamp without time zone,
    "Text" text COLLATE pg_catalog."default" NOT NULL,
    "AuthorID" uuid NOT NULL,
    CONSTRAINT "TheNote_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "TheNote_AuthorID_fkey" FOREIGN KEY ("AuthorID")
        REFERENCES "User" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "TheNote"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Deadline"
(
    "ID" uuid NOT NULL,
    "AuthorID" uuid NOT NULL,
    "Text" text COLLATE pg_catalog."default",
    "Date" timestamp without time zone NOT NULL,
    "DateEnd" timestamp without time zone NOT NULL,
    "Group" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Deadline_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "Deadline_AuthorID_fkey" FOREIGN KEY ("AuthorID")
        REFERENCES "User" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Deadline_Group_fkey" FOREIGN KEY ("Group")
        REFERENCES "Group" ("Name") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "Deadline"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Announcement"
(
    "ID" uuid NOT NULL,
    "Text" text COLLATE pg_catalog."default" NOT NULL,
    "AuthorID" uuid NOT NULL,
    "Group" text COLLATE pg_catalog."default" NOT NULL,
    "Date" timestamp without time zone NOT NULL,
    CONSTRAINT "Announcement_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "Announcement_AuthorID_fkey" FOREIGN KEY ("AuthorID")
        REFERENCES "User" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Announcement_Group_fkey" FOREIGN KEY ("Group")
        REFERENCES "Group" ("Name") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "Announcement"
    OWNER to tatfezxgvgaefs;
    
CREATE TABLE "Schedule"
(
    "ID" uuid NOT NULL,
    "LessonID" uuid NOT NULL,
    "AudienceID" text COLLATE pg_catalog."default" NOT NULL,
    "DayOfWeek" integer NOT NULL,
    "PairNumber" integer NOT NULL,
    "NumberOfWeek" integer NOT NULL,
    "LessonType" uuid NOT NULL,
    CONSTRAINT "Schedule_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "Schedule_AudienceID_fkey" FOREIGN KEY ("AudienceID")
        REFERENCES "Audience" ("Number") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Schedule_LessonID_fkey" FOREIGN KEY ("LessonID")
        REFERENCES "Lesson" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Schedule_LessonType_fkey" FOREIGN KEY ("LessonType")
        REFERENCES "LessonType" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE "Schedule"
    OWNER to tatfezxgvgaefs;
"""

GET_SCHEMA_BY_SESSION = """
SELECT "EducationalID" FROM "Authorization" WHERE "Session" = %s
"""
