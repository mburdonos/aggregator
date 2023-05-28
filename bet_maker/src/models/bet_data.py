from pydantic import BaseModel, Field, validator
from decimal import Decimal


class BetData(BaseModel):
    event_id: int
    money: Decimal = Field(gt=0)

    @validator("money")
    def check_money(cls, money):
        return money.quantize(Decimal("1.00"))
