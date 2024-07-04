# Blackjack Probability Calculator (WIP)

This project generates tables, using Python and pandas, to determine optimal play strategies for blackjack. This project also includes Monte Carlo simulations to cross-check the expected values and probabilities

## Project Features

- **Dealer Probability Distribution**: Calculates the overall distribution of the dealer's final hand.
- **Conditional Dealer Probabilities**: Determines the probabilities for the dealer's results based on their first card.
- **Player's Expected Profit**: Computes the expected profit for the player when they:
  - Stand
  - Hit
  - Hit with a soft hand (Ace counted as 11)
- **Optimal Player Strategy**: Evaluates the player's profit when they play optimally:
  - With and without a soft hand
- **Optimal Move Charts**:
  - Optimal Move Chart
  - Optimal Soft Move Chart
- **Monte Carlo Simulation**: Cross-checks all probabilities through extensive simulations.

## Constraints

- **Infinite Deck**: Assumes an infinite-sized deck.
- **Dealer Stands on Soft 17**: The dealer does not hit on soft 17.
- **No Double Downs or Splits**: Double downs and splits are not included in the current calculations (to be added later).

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/blackjack-probability-calculator.git
   cd blackjack-probability-calculator

2. **Create a Virtual Environment (Optional but recommended)**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt

## Usage
  ```python
  # import functions from ProbabilityFunctions
  import ProbabilityFunctions
  blackjack = BlackjackProbabilityCalculator()

  dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
  
  # Print the dataframes
  print(create_dealer_prob_dist_table(dealer_upcards)) # Overall Dealer Probability Distribution
  print(create_dealer_prob_table(dealer_upcards)) # Probabilities for the dealer's results conditioned on the dealer's first card
  print(create_stand_EV_table(dealer_upcards)) # Expectations, conditioned on the dealer's first card, for the player's profit, when the player stands
  print(create_hit_EV_table(dealer_upcards)) # Expectations, conditioned on the dealer's first card, for the player's profit, when the player hits
  print(create_soft_hit_EV_table(dealer_upcards)) # Expectations, conditioned on the dealer's first card, for the player's profit, when the player hits with a soft hand
  print(create_optimal_values_table(dealer_upcards)) # Expectations, conditioned on the dealer's first card, for the player's profit, when the player plays optimally
  print(create_soft_optimal_values_table(dealer_upcards)) # Expectations, conditioned on the dealer's first card, for the player's profit, when the player plays optimally and has a soft hand
  print(create_optimal_table(dealer_upcards)) # Optimal Move Chart
  print(create_soft_optimal_table(dealer_upcards)) # Optimal Soft Move Chart
  ```
  
## Future Development

- **Double Downs and Splits**: Adding functionality to handle double downs and splits in the calculations.
- **Mobile App**: Developing a mobile app using Swift and SwiftUI to turn this calculator into an interactive training tool for Blackjack players.

## Acknowledgements
- Inspired by [The mathematics of blackjack: Probabilities](https://probability.infarom.ro/blackjack.html)
