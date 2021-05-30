GET_AUDIENCES = """
select "Number" "id" from "Audience" where "HousingID" = %s
"""

ADD_AUDIENCES = """
insert into "Audiences" values (%s, %s, %s)
"""