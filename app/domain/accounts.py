from dataclasses import dataclass
from urllib.robotparser import normalize


class InvalidCurrencyError(ValueError):
    pass


@dataclass(frozen=True)
class Currency:
    code: str

    def __post_init__(self) -> None:
        normalized_code = self.code.upper()

        if len(normalized_code) != 3 or not normalized_code.isalpha():
            raise InvalidCurrencyError("Currency must be a 3-letter ISO code")

        object.__setattr__(self, "code", normalized_code)

