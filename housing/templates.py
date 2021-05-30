GET_ALL_HOUSING = """
select "ID" "id", "Address" "address" from "Housing"
"""

ADD_HOUSING = """
insert into "Housing" values (%s, %s)
returning "ID" "id", "Address" "address"
"""

EDIT_ADDRESS = """
update "Housing" set "Address" = %s where "ID" = %s
"""