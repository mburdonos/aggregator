from pydantic import BaseModel, Field


class BetData(BaseModel):
    event_id: int
    money: float = Field(ge=0)
