from BlackjackProbabilityCalculator import *
import time

if __name__ == "__main__":
    blackjack = BlackjackProbabilityCalculator()
    dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
    all_results = {}
    for upcard in dealer_upcards:
        if upcard != 'A':
            all_results[int(upcard)] = blackjack.probability_distribution(int(upcard))
        else:
            all_results['A'] = blackjack.probability_distribution(11)
    df = pd.DataFrame(all_results)
    df2 = pd.DataFrame(blackjack.probability_distribution().items(), columns=['Outcome', 'Probability'])
    df2.set_index('Outcome', inplace=True)
    df2 = df2.T
    print()
    print(df2)
    print()
    print(df)