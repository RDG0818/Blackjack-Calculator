# Blackjack Probability Calculator

This Python project is designed to simulate and analyze the probabilities of various decisions in the game of Blackjack. This project includes several key components aimed at different aspects of Blackjack simulation and strategy evaluation.

## Files:

1. **Blackjack.py**
   Contains the Blackjack class that facilitates gameplay and interaction between players and the dealer.
   Provides methods for initializing hands, managing cards, and executing game logic.
   ```python
   game = Blackjack()
   game.play_game()

3. **MonteCarlo.py**
   Implements Monte Carlo simulations for evaluating strategies in Blackjack.
   Includes functions for simulating standing and hitting scenarios to estimate win probabilities and expected values.
   Includes the following functions:
   ```python
   monte_carlo_stand(simulations: int, player_hand_value: int, dealer_upcard: int) # Simulate the outcome of standing in blackjack. Returns a float
   monte_carlo_hit(simulations: int, player_hand: list, dealer_upcard: int) # Simulate the outcome of hitting in blackjack. Returns a float
   ```

4. **ProbabilityFunctions.py**
   Defines probability distribution calculations related to Blackjack.
   Functions compute probabilities of various outcomes based on dealer's upcard and player's hand values. Each function returns a dictionary.
   ```python
   probability_distribution(dealer_upcard=None) # Calculates the probability distribution of the dealer depending on the value given. If no value is given, then it calculates the general probability distribution.
   stand_EV(dealer_upcard: int) # Calculate the expected value of standing with a given dealer upcard.
   hit_EV(dealer_upcard: int) # Calculate the expected value of hitting with a given dealer upcard.
   soft_hit_EV(dealer_upcard: int) # Calculate the expected value of hitting with a soft hand (hand containing an ace) and a given dealer upcard.
   ```

6. **TableCreation.py**
   Generates tables summarizing optimal strategies and expected values for Blackjack.
   Functions create Pandas DataFrames for visualizing strategy decisions based on different game scenarios.
   ```python
   dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
   create_optimal_table(dealer_upcards)
   create_soft_optimal_table(dealer_upcards)
   create_split_optimal_table(dealer_upcards)
   ```
   
## Constraints

- **Infinite Deck**: Both the Monte Carlo simulations and the probability functions assume an infinite deck size.
- **Dealer Stands on Soft 17**: The dealer does not hit on soft 17.

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
  

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Inspired by [The mathematics of blackjack: Probabilities](https://probability.infarom.ro/blackjack.html)
