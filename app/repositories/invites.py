# +-------------+-------------+------+-----+----------------------+-------+
# | Field       | Type        | Null | Key | Default              | Extra |
# +-------------+-------------+------+-----+----------------------+-------+
# | user_id     | int(11)     | NO   | MUL | NULL                 |       |
# | time        | timestamp   | NO   |     | NULL                 |       |
# | used_by     | int(11)     | YES  | MUL | NULL                 |       |
# | invite_code | varchar(16) | NO   |     | left(md5(rand()),16) |       |
# +-------------+-------------+------+-----+----------------------+-------+

# Table: users_invitation

import textwrap
from typing import Any

import app

READ_PARAMS = textwrap.dedent(
    """\
        user_id, time, used_by, invite_code
    """,
)


async def fetch(invite_code: str) -> dict[str, Any]:
    """Fetch an invitation from the database by its code."""
    query = f"SELECT {READ_PARAMS} FROM users_invitation WHERE invite_code = :invite_code"
    params = {"invite_code": invite_code}
    rec = await app.state.services.database.fetch_one(query, params)
    return dict(rec) if rec else None


async def set_code_used(invite_code: str, user_id: int) -> None:
    """Set the code as used."""
    query = f"UPDATE users_invitation SET used_by = :user_id WHERE invite_code = :invite_code"
    params = {"invite_code": invite_code, "user_id": user_id}
    await app.state.services.database.execute(query, params)
