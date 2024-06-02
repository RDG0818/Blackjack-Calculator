from input_handling import *
from hand_evaluation import *
from probability import *
dealer_card = dealer_input()
player_hand = player_input()
print("Chance to bust is", str(chance_of_bust(dealer_card, player_hand)))