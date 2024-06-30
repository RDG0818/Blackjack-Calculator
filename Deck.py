from Card import *
import random
class Deck:
    def __init__(self, num = 1) -> None:
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K")
        self.list = [Card(rank) for rank in self.ranks] * 4 * num
        self.original_copy_list = self.list

    def deal_card(self) -> Card:
        if self.list:
            card = self.list.pop()
            return card
        else:
            raise IndexError("No more cards in the deck.")
    
    def shuffle(self) -> None:
        random.shuffle(self.list)

    def reset(self) -> None:
        self.list = self.original_copy_list

    def size(self) -> int:
        return len(self.list)

    def add_card(self, card: Card) -> None:
        self.list.append(card)

    def remove_card(self, card_to_remove: Card) -> None:
        self.list.remove(card_to_remove)

    def is_empty(self) -> bool:
        return self.count == 0
    
    def get_value_dict(self) -> dict: 
        rank_count = {num: 0 for num in range(1, 11)}
        tens = ["T", "J", "Q", "K"]
        for card in self.list:
            if (card.rank == 'A'):
                rank_count[1] += 1
            elif (card.rank in tens):
                rank_count[10] += 1
            else:
                rank_count[int(card.rank)] += 1
        return rank_count
    
    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.list)
        
    