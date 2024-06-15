from BlackjackProbabilityCalculator import *

blackjack = BlackjackProbabilityCalculator()
blackjack.get_initial_hands()
print(blackjack.monte_carlo_simulation(10000))