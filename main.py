from BlackjackProbabilityCalculator import *

blackjack = BlackjackProbabilityCalculator()
blackjack.get_initial_hands()
print([str(round(num * 100, 4)) + '%' for num in blackjack.monte_carlo_simulation(30000)])