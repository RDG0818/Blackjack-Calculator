import pandas as pd

def probability_distribution(dealer_upcard: int = None) -> dict:
    """
    Calculate the probability distribution of the dealer's final hand values in blackjack.

    Args:
        dealer_upcard (int, optional): The dealer's upcard value. If not provided, the general probability distribution is generated.

    Returns:
        dict: A dictionary representing the probability distribution of the dealer's final hand values, including possible outcomes for busting and Blackjack.
    """
    def calculate_probabilities(path: list, result: dict) -> None:
        """
        Recursively calculate probabilities of different hand values for the dealer.

        Args:
            path (list): The current sequence of cards drawn.
            result (dict): The dictionary to store probabilities of different hand outcomes.
        """
        # Handle soft ace conversion (11 to 1) to prevent busting
        if 11 in path and sum(path) >= 22:
            path = path[:]
            path[path.index(11)] = 1

        total = sum(path)
        
        if total >= 17:
            # Calculate the probability for the current path
            probability = 1
            start = 0 if dealer_upcard is None else 1
            for i in range(start, len(path)):
                probability *= (1 / 13) if path[i] != 10 else (4 / 13)

            if len(path) == 2 and 10 in path and 11 in path:
                result["BJ"] += probability  # Blackjack
            elif total <= 21:
                result[total] += probability  # Final hand value
            else:
                result["bust"] += probability  # Dealer busts
            return

        # Recursively explore the next possible card values
        for card in range(2, 12):
            path.append(card)
            calculate_probabilities(path, result)
            path.pop()

    # Initialize result dictionary
    result = {value: 0 for value in range(17, 22)}
    result["bust"] = 0
    result["BJ"] = 0

    # Start the recursive probability calculation
    if dealer_upcard:
        calculate_probabilities([dealer_upcard], result)
    else:
        calculate_probabilities([], result)

    return result


def stand_EV(dealer_upcard: int) -> dict:
    """
    Calculate the expected value of standing with a given dealer upcard.

    Args:
        dealer_upcard (int): The dealer's upcard value (must be between 2 and 11, inclusive).

    Returns:
        dict: A dictionary mapping player hand values (2 to 21, and "BJ" for Blackjack) to their expected values when standing.
    """
    # Get the probability distribution for the dealer's hand outcomes given the upcard
    dealer_probs = probability_distribution(dealer_upcard)
    
    # Initialize the expected value dictionary for all player hand values from 21 down to 2, plus "BJ" for Blackjack
    ev_dict = {hand_value: 0 for hand_value in range(21, 1, -1)}
    ev_dict["BJ"] = 0

    # Calculate the expected value for each possible player hand value
    for player_value in ev_dict.keys():
        if player_value == "BJ":
            # Calculate EV specifically for Blackjack (payout is typically 1.5x)
            for dealer_value, prob in dealer_probs.items():
                if dealer_value != "BJ":
                    ev_dict[player_value] += prob
            ev_dict[player_value] *= 1.5
        else:
            # Calculate EV for regular hand values
            for dealer_value, prob in dealer_probs.items():
                if dealer_value == "BJ":
                    ev_dict[player_value] -= prob  # Dealer Blackjack results in loss
                elif dealer_value == "bust" or dealer_value < player_value:
                    ev_dict[player_value] += prob  # Player wins
                elif dealer_value > player_value:
                    ev_dict[player_value] -= prob  # Player loses

    return ev_dict


def hit_EV(dealer_upcard: int, double_down: bool = False) -> dict:
    """
    Calculate the expected value of hitting with a given dealer upcard. Optionally includes the impact of doubling down.

    Args:
        dealer_upcard (int): The dealer's upcard value (must be between 2 and 11, inclusive).
        double_down (bool, optional): Whether the player will double down (draw one card and double the stakes). Defaults to False.

    Returns:
        dict: A dictionary mapping player hand values (11 to 21) to their expected values when hitting.
              The EV is doubled if double_down is True.
    """
    # Get the expected values for standing
    stand_ev = stand_EV(dealer_upcard)
    hit_ev = {}

    # Calculate expected value for each player hand value
    for player_value in range(21, 10, -1):
        total_ev = 0
        for card in range(1, 11):
            new_value = player_value + card

            if new_value > 21:
                # Calculate probability of busting
                total_ev += (-1 / 13) if card != 10 else (-4 / 13)
            else:
                # Get the maximum EV from hitting or standing
                prob = max(hit_ev.get(new_value, 0), stand_ev.get(new_value, 0)) if not double_down else stand_ev.get(new_value, 0)
                # Add probability weighted expected value
                total_ev += (1 / 13 * prob) if card != 10 else (4 / 13 * prob)

        # Double the expected value if doubling down
        hit_ev[player_value] = total_ev * 2 if double_down else total_ev

    return hit_ev


def soft_hit_EV(dealer_upcard: int, double_down: bool = False) -> dict:
    """
    Calculate the expected value of hitting with a soft hand (a hand containing an ace) and a given dealer upcard.

    Args:
        dealer_upcard (int): The dealer's upcard value (must be between 2 and 11, inclusive).
        double_down (bool, optional): Whether the player will double down (draw one card and double the stakes). Defaults to False.

    Returns:
        dict: A dictionary mapping player hand values (11 to 21) to their expected values when hitting with a soft hand.
              The EV is doubled if double_down is True.
    """
    # Get the expected values for standing and hitting
    stand_ev = stand_EV(dealer_upcard)
    hit_ev = hit_EV(dealer_upcard)
    soft_hit_ev = {}

    # Calculate expected value for each player hand value with a soft hand
    for player_value in range(21, 10, -1):
        total_ev = 0
        
        for card in range(1, 11):
            new_value = player_value + card

            if new_value > 21:
                # Handle case where the new value exceeds 21
                prob = max(hit_ev.get(new_value - 10, 0), stand_ev.get(new_value - 10, 0)) if not double_down else stand_ev.get(new_value - 10, 0)
                total_ev += (1 / 13 * prob) if card != 10 else (4 / 13 * prob)
            else:
                # Get the maximum EV from soft hit, hit, or stand
                prob = max(soft_hit_ev.get(new_value, 0), hit_ev.get(new_value, 0), stand_ev.get(new_value, 0)) if not double_down else stand_ev.get(new_value, 0)
                total_ev += (1 / 13 * prob) if card != 10 else (4 / 13 * prob)

        # Double the expected value if doubling down
        soft_hit_ev[player_value] = total_ev * 2 if double_down else total_ev

    return soft_hit_ev


def total_hit_EV(dealer_upcard: int, double_down = False) -> dict:
    """
    Calculates the expected value of hitting for all player hand values between 2 and 21, inclusive.

    Args:
        dealer_upcard (int): The dealer's upcard value (must be between 2 and 11, inclusive).

    Returns:
        dict: A dictionary mapping player hand values (2 to 21) to their expected values when hitting.
              Includes the effects of both soft and hard hands.
    """
    # Get expected values for standing, hitting, and soft hitting
    stand_ev = stand_EV(dealer_upcard)
    hit_ev = hit_EV(dealer_upcard, double_down)
    soft_hit_ev = soft_hit_EV(dealer_upcard)
    
    # Calculate the expected value for each player hand value from 10 to 2
    for player_value in range(10, 1, -1):
        total_ev = 0
        for card in range(2, 12):
            new_value = player_value + card

            if new_value > 21:
                # Calculate probability of busting
                total_ev += (-1 / 13) if card != 10 else (-4 / 13)
            else:
                # Determine the best possible EV considering the card drawn
                if card == 11:
                    prob = max(stand_ev.get(new_value, 0), soft_hit_ev.get(new_value, 0)) if not double_down else stand_ev.get(new_value, 0)
                else:
                    prob = max(stand_ev.get(new_value, 0), hit_ev.get(new_value, 0)) if not double_down else stand_ev.get(new_value, 0)
                total_ev += (1 / 13 * prob) if card != 10 else (4 / 13 * prob)
        
        hit_ev[player_value] = total_ev * 2 if double_down else total_ev

    return hit_ev


def split_EV(dealer_upcard: int) -> dict:
    """
    Calculate the expected value of splitting a pair of equal cards with a given dealer upcard.

    Args:
        dealer_upcard (int): The dealer's upcard value (must be between 2 and 11, inclusive).

    Returns:
        dict: A dictionary mapping card values (2 to 11) to their expected values when splitting pairs.
              The EV is calculated by taking the best possible EV from hitting or standing and doubling it.
    """
    # Get the expected values for standing, hitting, and soft hitting
    stand_ev = stand_EV(dealer_upcard)
    hit_ev = total_hit_EV(dealer_upcard)
    soft_hit_ev = soft_hit_EV(dealer_upcard)
    
    split_ev = {}

    # Calculate expected value for each card value when splitting
    for card in range(2, 12):
        # Use the maximum expected value from hitting or standing
        if card == 11:
            ev = max(stand_ev.get(card, 0), soft_hit_ev.get(card, 0))
        else:
            ev = max(stand_ev.get(card, 0), hit_ev.get(card, 0))
        # Double the expected value as splitting involves two hands
        split_ev[card] = ev * 2

    return split_ev


# def alternate_split_EV(dealer_upcard: int) -> dict:
#     """
#     An alternate way to calculate the expected value of splits. Gives different numbers than split_EV.
    
#     :param dealer_upcard: The dealer's upcard value (must be between 2 and 11, inclusive).
#     :return: A dictionary representing the expected values for splitting pairs of cards (between pairs of 2 and pairs of 11)."""
#     s_EV = stand_EV(dealer_upcard)
#     h_EV = total_hit_EV(dealer_upcard)
#     s_h_EV = soft_hit_EV(dealer_upcard)
#     split_EV = {}
    
#     for card in range(2, 12):
#         total = 0
#         if card != 11:
#             for hand_1_card_2 in range(2, 12):
#                 hand_1_prob = max(s_EV[card + hand_1_card_2], h_EV[card + hand_1_card_2]) if hand_1_card_2 != 11 else max(s_EV[card + hand_1_card_2], s_h_EV[card + hand_1_card_2])
#                 hand_1_prob *= 4 if hand_1_card_2 == 10 else 1
#                 for hand_2_card_2 in range(2, 12):
#                     hand_2_prob = max(s_EV[card + hand_2_card_2], h_EV[card + hand_2_card_2]) if hand_2_card_2 != 11 else max(s_EV[card + hand_2_card_2], s_h_EV[card + hand_2_card_2])
#                     hand_2_prob *= 4 if hand_2_card_2 == 10 else 1
#                     total += (hand_1_prob + hand_2_prob)/169
#         else:
#             for hand_1_card_2 in range(1, 11):
#                 hand_1_prob = s_EV[card + hand_1_card_2] 
#                 hand_1_prob *= 4 if hand_1_card_2 == 10 else 1
#                 for hand_2_card_2 in range(1, 11):
#                     hand_2_prob = s_EV[card + hand_2_card_2]
#                     hand_2_prob *= 4 if hand_2_card_2 == 10 else 1
#                     total += hand_1_prob + hand_2_prob
#             total /= 169
        
#         split_EV[card] = total
    
#     return split_EV