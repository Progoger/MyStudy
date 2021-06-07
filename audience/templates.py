GET_AUDIENCES = """
select "Number" "id" from "Audience" where "HousingID" = %s
"""

ADD_AUDIENCES = """
insert into "Audience" values (%s, %s)
returning "Number" "id"
"""