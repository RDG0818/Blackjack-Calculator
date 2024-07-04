# Blackjack Probability Calculator (WIP)

This project provides a comprehensive Blackjack Probability Calculator, using Python and pandas, to determine optimal play strategies under specific constraints. The calculator generates tables and performs simulations to help users understand the exact probabilities of each decision in Blackjack.

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


## Future Development

- **Double Downs and Splits**: Adding functionality to handle double downs and splits in the calculations.
- **Mobile App**: Developing a mobile app using Swift and SwiftUI to turn this calculator into an interactive training tool for Blackjack players.

## Acknowledgements
- Inspired by [The mathematics of blackjack: Probabilities](https://probability.infarom.ro/blackjack.html)