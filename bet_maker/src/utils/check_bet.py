from models.bet import Bet
from models.storage.events import Event


def check_bet_result(data: list[Bet], event: Event) -> list[Bet]:
    for row in data:
        if event.state.value == 2:
            row.money = row.money * float(event.coefficient)
            row.result = "win"
            continue
        elif event.state.value == 3:
            row.money = 0
            row.result = "lose"
    return data
