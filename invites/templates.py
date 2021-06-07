GENERATE_CODES = """
insert into "InviteCodes"
select code, %s
from UNNEST(%s) code
returning *
"""

IS_ACTIVE_CODE = """
SELECT EXISTS(select null from "InviteCodes" where "Code" = %s and "IsActive" = true)
"""

DEL_CODE = """
DELETE FROM "InviteCodes" where "Code" = %s
"""