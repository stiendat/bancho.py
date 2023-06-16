# +------------+------------+------+-----+----------------------+-------+
# | Field      | Type       | Null | Key | Default              | Extra |
# +------------+------------+------+-----+----------------------+-------+
# | discord_id | bigint(19) | NO   | PRI | NULL                 |       |
# | time       | timestamp  | NO   |     | current_timestamp()  |       |
# | verify_key | char(16)   | YES  |     | left(md5(rand()),16) |       |
# +------------+------------+------+-----+----------------------+-------+

# Table: discord_verify

import textwrap
from typing import Any

import app

READ_PARAMS = textwrap.dedent(
    """\
        discord_id, time, verify_key
    """,
)


async def fetch(verify_key: str) -> dict[str, Any]:
    """Fetch a verification from the database by its code."""
    query = f"SELECT {READ_PARAMS} FROM discord_verify WHERE verify_key = :verify_key"
    params = {"verify_key": verify_key}
    rec = await app.state.services.database.fetch_one(query, params)
    return dict(rec) if rec else None


async def update(verify_key: str, used_by: int) -> None:
    """Set the code as used."""
    query = f"UPDATE discord_verify SET discord_id = :used_by WHERE verify_key = :verify_key"
    params = {"verify_key": verify_key, "used_by": used_by}
    await app.state.services.database.execute(query, params)
