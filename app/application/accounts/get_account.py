from dataclasses import dataclass
from typing import Any
from uuid import UUID
from psycopg_pool import ConnectionPool

from app.infrastructure.db.uow import UnitOfWork
class AccountNotFound(Exception):
    pass

@dataclass(frozen=True)
class GetAccountCommand:
    account_id: UUID


class GetAccountUseCase:
    def __init__(self, pool: ConnectionPool) -> None:
        self.pool = pool

    def execute(self, command: GetAccountCommand) -> dict[str, Any]:
        with UnitOfWork(self.pool) as uow:
            account = uow.accounts.get_by_id(command.account_id)
        if account is None:
            raise AccountNotFound("Account not found")
        return account