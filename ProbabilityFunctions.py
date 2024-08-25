import pandas as pd

def probability_distribution(dealer_upcard=None) -> dict:
    """
    Calculate the probability distribution of the dealer's final hand values in blackjack.

    :param dealer_upcard: The dealer's upcard value, if any. If no value is provided then the general probability distribution is generated.
    :return: A dictionary representing the probability distribution of the dealer's final hand values.
    """
    def backtracking(path: list, result: dict) -> None:
        """
        Recursively calculate probabilities of different hand values for the dealer.

        :param path: The current path of cards drawn.
        :param result: The dictionary to store the probabilities of different hand outcomes.
        """
        # Handle the conversion of a soft ace (11) to a hard ace (1) if it prevents busting
        if 11 in path and sum(path) >= 22:
            path = path[:]
            path[path.index(11)] = 1

        # Calculate probabilities and update the result dictionary
        total = sum(path)
        if total >= 17:
            total_probability = 1
            start = 0 if dealer_upcard is None else 1
            for i in range(start, len(path)):
                total_probability *= (1/13) if path[i] != 10 else (4/13)
            if len(path) == 2 and 10 in path and 11 in path:
                result["BJ"] += total_probability
            elif total <= 21:
                result[total] += total_probability
            else:
                result["bust"] += total_probability
            return

        # Recursively explore the next possible card values
        for i in range(2, 12):
            path.append(i)
            backtracking(path, result)
            path.pop()

    # Initialize the result dictionary
    result = {num: 0 for num in range(17, 22)}
    result["bust"] = 0
    result["BJ"] = 0

    # Start the backtracking process
    if dealer_upcard:
        backtracking([dealer_upcard], result)
    else:
        backtracking([], result)
    return result

def stand_EV(dealer_upcard: int) -> dict:
    """
    Calculate the expected value of standing with a given dealer upcard.

    :param dealer_upcard: The dealer's upcard value.
    :return: A dictionary representing the expected values for different player hand values when standing.
    """
    probabilities = probability_distribution(dealer_upcard)
    stand_EV = {num: 0 for num in range(21, 3, -1)}
    stand_EV["BJ"] = 0

    for player_value in stand_EV.keys():
        if player_value == "BJ":
            for value, prob in probabilities.items():
                if value != "BJ":
                    stand_EV[player_value] += prob
            stand_EV[player_value] *= 1.5
        else:
            for value, prob in probabilities.items():
                if value == "BJ":
                    stand_EV[player_value] -= prob
                elif value == "bust":
                    stand_EV[player_value] += prob
                elif value < player_value:
                    stand_EV[player_value] += prob
                elif value > player_value:
                    stand_EV[player_value] -= prob
    return stand_EV

def hit_EV(dealer_upcard: int, double_down = False) -> dict:
    """
    Calculate the expected value of hitting with a given dealer upcard.

    :param dealer_upcard: The dealer's upcard value.
    :return: A dictionary representing the expected values for different player hand values when hitting.
    """
    s_EV = stand_EV(dealer_upcard)
    hit_EV = {}

    for player_value in range(21, 3, -1):
        total = 0
        for card in range(1, 11):
            if player_value + card > 21:
                total += -1/13 if card != 10 else -4/13
            else:
                prob = max(hit_EV.get(player_value + card, 0), s_EV.get(player_value + card, 0)) if not double_down else s_EV.get(player_value + card, 0)
                total += (1/13 * prob) if card != 10 else (4/13 * prob)
        hit_EV[player_value] = total if not double_down else total * 2
    return hit_EV

def soft_hit_EV(dealer_upcard: int, double_down = False) -> dict:
    """
    Calculate the expected value of hitting with a soft hand (hand containing an ace) and a given dealer upcard.

    :param dealer_upcard: The dealer's upcard value.
    :return: A dictionary representing the expected values for different player hand values when hitting with a soft hand.
    """
    s_EV = stand_EV(dealer_upcard)
    h_EV = hit_EV(dealer_upcard)
    soft_hit_EV = {}

    for player_value in range(21, 11, -1):
        total = 0
        for card in range(1, 11):
            if player_value + card > 21:
                prob = max(h_EV.get(player_value + card - 10, 0), s_EV.get(player_value + card - 10, 0)) if not double_down else s_EV.get(player_value + card - 10, 0)
                total += (1/13 * prob) if card != 10 else (4/13 * prob)
            else:
                prob = max(soft_hit_EV.get(player_value + card, 0), h_EV.get(player_value + card, 0), s_EV.get(player_value + card, 0)) if not double_down else s_EV.get(player_value + card, 0)
                total += (1/13 * prob) if card != 10 else (4/13 * prob)
        soft_hit_EV[player_value] = total if not double_down else total * 2
    return soft_hit_EV
