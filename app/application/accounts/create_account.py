from dataclasses import dataclass
from uuid import UUID
from psycopg_pool import ConnectionPool
from app.domain.accounts import Currency
from app.infrastructure.db.uow import UnitOfWork

@dataclass(frozen=True)
class CreateAccountCommand:
    owner_id: UUID
    currency: str = "RUB"


class CreateAccountUseCase:
    def __init__(self, pool: ConnectionPool) -> None:
        self.pool = pool

    def execute(self, command: CreateAccountCommand) -> dict:
        currency = Currency(command.currency)
        with UnitOfWork(self.pool) as uow:
            return uow.accounts.create(
                owner_id=command.owner_id,
                currency=currency.code,
            )