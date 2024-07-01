# Blackjack Probability Calculator

This project provides a comprehensive analysis of blackjack probabilities and expected values using Python. The analysis includes dealer probability distributions, conditional probabilities based on the dealer's first card, and the player's expected value when standing. The calculations assume the dealer does not hit on a soft 17 and an infinite-sized deck. Note that this is still WIP.

## Features

- **Probability Distributions**: Computes the dealer's end probability distribution and probabilities conditioned on the dealer's first card.
- **Expected Value Calculation**: Calculates the player's expected value when they choose to stand, incorporating complex interactions between player and dealer hands.
- **Monte Carlo Simulations**: Cross-checks calculated probabilities with Monte Carlo simulations for validation.
- **Object-Oriented Design**: Utilizes an extensive class hierarchy for cards, hands, decks, players, and the probability calculator.

## Dependencies

- Python 3.x
- pandas
