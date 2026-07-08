CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL,
    balance NUMERIC(18, 2) NOT NULL DEFAULT 0,
    currency CHAR(3) NOT NULL DEFAULT 'RUB',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT accounts_balance_non_negative CHECK (balance >= 0)
);

CREATE TABLE IF NOT EXISTS transfers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_account_id UUID NOT NULL REFERENCES accounts(id),
    to_account_id UUID NOT NULL REFERENCES accounts(id),
    amount NUMERIC(18, 2) NOT NULL,
    currency CHAR(3) NOT NULL,
    status TEXT NOT NULL DEFAULT 'completed',
    idempotency_key TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT transfers_amount_positive CHECK (amount > 0),
    CONSTRAINT transfers_different_accounts CHECK (from_account_id <> to_account_id),
    CONSTRAINT transfers_status_valid CHECK (status IN ('completed', 'failed'))
);

CREATE TABLE IF NOT EXISTS ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transfer_id UUID NOT NULL REFERENCES transfers(id),
    account_id UUID NOT NULL REFERENCES accounts(id),
    amount_delta NUMERIC(18, 2) NOT NULL,
    direction TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ledger_entries_amount_not_zero CHECK (amount_delta <> 0),
    CONSTRAINT ledger_entries_direction_valid CHECK (direction IN ('debit', 'credit'))
);

CREATE INDEX IF NOT EXISTS idx_transfers_from_account_id
    ON transfers(from_account_id);

CREATE INDEX IF NOT EXISTS idx_transfers_to_account_id
    ON transfers(to_account_id);

CREATE INDEX IF NOT EXISTS idx_ledger_entries_account_id
    ON ledger_entries(account_id);

CREATE INDEX IF NOT EXISTS idx_ledger_entries_transfer_id
    ON ledger_entries(transfer_id);