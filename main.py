from functions import *
dealer_card = dealer_input()
player_hand = create_hand()
print(str(round(chance_of_bust(dealer_card, player_hand) * 100, 3)) + '%')