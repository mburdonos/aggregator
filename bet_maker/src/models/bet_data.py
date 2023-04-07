from pydantic import BaseModel, Field, validator


class BetData(BaseModel):
    event_id: str
    money: float = Field(gt=0)

    @validator("money")
    def check_money(cls, money):
        return round(money, 2)
