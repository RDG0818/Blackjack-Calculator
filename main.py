from BlackjackProbabilityCalculator import *
import time

if __name__ == "__main__":
    blackjack = BlackjackProbabilityCalculator()
    blackjack.get_initial_hands()
    start_time = time.time()
    print(blackjack.sequential_single_hit(10000))
    end_time = time.time()
    print("Elapsed time:", end_time - start_time)
    start_time = time.time()
    print(blackjack.sequential_stand(10000))
    end_time = time.time()
    print("Elapsed time:", end_time - start_time)

    