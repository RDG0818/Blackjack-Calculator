from Card import *
import random
class Deck:
    def __init__(self) -> None:
        self.suits = ("S", "C", "H", "D")
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K")
        self.list = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
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

    def size(self) -> int:
        return len(self.list)

    def add_card(self, card: Card) -> None:
        self.list.append(card)

    def remove_card(self, card_to_remove: Card) -> None:
        self.list.remove(card_to_remove)

    def is_empty(self) -> bool:
        return self.count == 0
    
    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.list)
        
    