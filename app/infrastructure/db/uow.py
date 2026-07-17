from types import TracebackType
from typing import Self
from psycopg import Connection
from psycopg_pool import ConnectionPool
from app.infrastructure.repositories.accounts import AccountRepository

class UnitOfWork:
    def __init__(self, pool: ConnectionPool) -> None:
        self.pool = pool

    def __enter__(self) -> Self:
        self._connection_context = self.pool.connection()
        self.conn: Connection = self._connection_context.__enter__()

        self._transaction_context = self.conn.transaction()
        self._transaction_context.__enter__()

        self.accounts = AccountRepository(self.conn)

        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
    ) -> None:
        self._transaction_context.__exit__(exc_type, exc_value, traceback)
        self._connection_context.__exit__(exc_type, exc_value, traceback)