from fastapi import APIRouter, Depends, HTTPException, status
from psycopg_pool import ConnectionPool
from uuid import UUID

from app.api.deps import get_db_pool
from app.application.accounts.create_account import (
    CreateAccountCommand,
    CreateAccountUseCase,
)
from app.application.accounts.get_account import GetAccountUseCase, GetAccountCommand, AccountNotFound

from app.domain.accounts import InvalidCurrencyError
from app.schemas.accounts import AccountResponse, CreateAccountRequest


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED
)
def create_account(request: CreateAccountRequest,pool: ConnectionPool = Depends(get_db_pool),) -> dict:
    use_case = CreateAccountUseCase(pool)

    try:
        command = CreateAccountCommand(
            owner_id=request.owner_id,
            currency=request.currency,
        )
        return use_case.execute(command)
    except InvalidCurrencyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
)
def get_account(account_id: UUID, pool:ConnectionPool = Depends(get_db_pool),) -> dict:
    use_case = GetAccountUseCase(pool)

    try:
        command = GetAccountCommand(account_id=account_id)
        return use_case.execute(command)
    except AccountNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc