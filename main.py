from BlackjackProbabilityCalculator import *
import time

if __name__ == "__main__":
    blackjack = BlackjackProbabilityCalculator()
    blackjack.get_initial_hands()
    start_time = time.time()
    tup = blackjack.sequential_monte_carlo_simulation(10000)
    end_time = time.time()
    print([str(round(num * 100, 4)) + '%' for num in tup])
    print(f"Sequential elapsed time: {end_time - start_time} seconds")
    start_time = time.time()
    tup = blackjack.parallelized_monte_carlo_simulation(10000)
    end_time = time.time()
    print([str(round(num * 100, 4)) + '%' for num in tup])
    print(f"Parallelized elapsed time: {end_time - start_time} seconds")