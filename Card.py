from collections.abc import Iterable


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        if self.rank in "23456789":
            return int(self.rank)
        elif self.rank in "TJQK":
            return 10
        elif self.rank == "A":
            return 11
        return 0
    
    def __eq__(self, other: "Card") -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __str__(self) -> str:
        return self.rank + self.suit
