from BlackjackProbabilityCalculator import *

blackjack = BlackjackProbabilityCalculator()
blackjack.get_initial_hands()
blackjack.player.hit(blackjack.deck)
blackjack.player.hit(blackjack.deck)
print(blackjack.player.hand)
print(blackjack.player.hand_value())
print(blackjack.player.is_bust())
print(blackjack.deck)