from Card import *
import random
class Deck:
    def __init__(self) -> None:
        suits = ["S", "C", "H", "D"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
        self.list = [Card(rank, suit) for suit in suits for rank in ranks]
        self.original_copy = self.list

    def deal_card(self) -> Card:
        if self.list:
            return self.list.pop()
        else:
            raise IndexError("No more cards in the deck.")
    
    def shuffle(self) -> None:
        random.shuffle(self.list)

    def reset(self) -> None:
        self.list = self.original_copy

    def count(self) -> int:
        return len(self.list)
