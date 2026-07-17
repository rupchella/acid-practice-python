from typing import Any

from uuid import UUID

from psycopg import Connection


class AccountRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create(self, owner_id: UUID, currency: str) -> dict[str, Any]:
        query = """
            INSERT INTO accounts (owner_id, currency)
            VALUES (%s, %s)
            RETURNING id, owner_id, balance, currency, created_at, updated_at;
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (owner_id, currency))
            account = cur.fetchone()

        if account is None:
            raise RuntimeError("Failed to create account")

        return account