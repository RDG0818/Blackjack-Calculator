from input_handling import *
from hand_evaluation import *
dealer_card = dealer_input()
player_hand = player_input()

score = hand_evaluation(player_hand)
