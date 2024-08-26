from ProbabilityFunctions import *
import pandas as pd

def create_dealer_prob_dist_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a probability distribution table for the dealer's possible outcomes.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the probability distribution of the dealer's outcomes.
    """
    overall_prob_df = pd.DataFrame(probability_distribution().items(), columns=['Outcome', 'Probability']).round(4)
    overall_prob_df.set_index('Outcome', inplace=True)
    return overall_prob_df.T

def create_dealer_prob_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of dealer probabilities for each upcard value.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its probability distribution.
    """
    dealer_probabilities = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        dealer_probabilities[upcard] = probability_distribution(upcard_value)
    return dealer_probabilities

def create_dealer_prob_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a probability table for the dealer's outcomes.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the probability distribution of the dealer's outcomes.
    """
    return pd.DataFrame(create_dealer_prob_dict(dealer_upcards))

def create_stand_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for standing with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when standing.
    """
    stand_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        stand_expected_values[upcard] = stand_EV(upcard_value)
    return stand_expected_values

def create_stand_EV_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of expected values for standing with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when standing.
    """
    return pd.DataFrame(create_stand_EV_dict(dealer_upcards))

def create_hit_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for hitting with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when hitting.
    """
    hit_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        hit_expected_values[upcard] = hit_EV(upcard_value)
    return hit_expected_values

def create_hit_EV_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of expected values for hitting with each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when hitting.
    """
    return pd.DataFrame(create_hit_EV_dict(dealer_upcards))

def create_soft_hit_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for hitting with a soft hand and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when hitting with a soft hand.
    """
    soft_hit_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        soft_hit_expected_values[upcard] = soft_hit_EV(upcard_value)
    return soft_hit_expected_values

def create_soft_hit_EV_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of expected values for hitting with a soft hand and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when hitting with a soft hand.
    """
    return pd.DataFrame(create_soft_hit_EV_dict(dealer_upcards))

def create_double_down_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for double downing.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when double downing.
    """

    double_down_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        double_down_expected_values[upcard] = hit_EV(upcard_value, True)
    return double_down_expected_values

def create_double_down_EV_table(dealer_upcards: list) -> dict:
    """
    Create a table of expected values for double downing.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when double downing.
    """   

    return pd.DataFrame(create_double_down_EV_dict(dealer_upcards))

def create_double_down_soft_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for double downing with a soft hand.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its expected value when double downing with a soft hand.
    """

    double_down_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        double_down_expected_values[upcard] = soft_hit_EV(upcard_value, True)
    return double_down_expected_values

def create_double_down_soft_EV_table(dealer_upcards: list) -> dict:
    """
    Create a table of expected values for double downing with a soft hand.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the expected values when double downing with a soft hand.
    """   

    return pd.DataFrame(create_double_down_soft_EV_dict(dealer_upcards))

def create_optimal_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of optimal expected values for each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its optimal expected value.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    hit_expected_values = create_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_EV_dict(dealer_upcards)
    optimal_expected_values = {}
    for upcard in dealer_upcards:
        optimal_expected_values[upcard] = {"BJ": stand_expected_values[upcard]["BJ"]}
        for value in range(21, 3, -1):
            optimal_expected_values[upcard][value] = max(stand_expected_values[upcard][value], hit_expected_values[upcard][value], double_down_values[upcard][value])
    return optimal_expected_values

def create_optimal_values_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal expected values for each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal expected values.
    """
    return pd.DataFrame(create_optimal_dict(dealer_upcards))

def create_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves (Stand or Hit) for each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal moves.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    hit_expected_values = create_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_EV_dict(dealer_upcards)
    optimal_moves = {}
    for upcard in dealer_upcards:
        optimal_moves[upcard] = {}
        for value in range(21, 3, -1):
            temp = max(stand_expected_values[upcard][value], hit_expected_values[upcard][value], double_down_values[upcard][value])
            if (temp == stand_expected_values[upcard][value]):
                optimal_moves[upcard][value] = "Stand"
            elif (temp == hit_expected_values[upcard][value]):
                optimal_moves[upcard][value] = "Hit"
            else:
                optimal_moves[upcard][value] = "DD"
    return pd.DataFrame(optimal_moves)

def create_soft_optimal_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of optimal expected values for soft hands and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its optimal expected value for soft hands.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_expected_values = create_soft_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_soft_EV_dict(dealer_upcards)
    soft_optimal_expected_values = {}
    for upcard in dealer_upcards:
        soft_optimal_expected_values[upcard] = {"BJ": stand_expected_values[upcard]["BJ"]}
        for value in range(21, 11, -1):
            soft_optimal_expected_values[upcard][value] = max(stand_expected_values[upcard][value], soft_hit_expected_values[upcard][value], double_down_values[upcard][value])
    return soft_optimal_expected_values

def create_soft_optimal_values_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal expected values for soft hands and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal expected values for soft hands.
    """
    return pd.DataFrame(create_soft_optimal_dict(dealer_upcards))

def create_soft_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves (Stand or Hit) for soft hands and each dealer upcard.

    :param dealer_upcards: List of dealer upcard values.
    :return: DataFrame representing the optimal moves for soft hands.
    """
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_expected_values = create_soft_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_soft_EV_dict(dealer_upcards)
    soft_optimal_moves = {}
    for upcard in dealer_upcards:
        soft_optimal_moves[upcard] = {}
        for value in range(21, 11, -1):
            temp = max(stand_expected_values[upcard][value], soft_hit_expected_values[upcard][value], double_down_values[upcard][value])
            if (temp == stand_expected_values[upcard][value]):
                soft_optimal_moves[upcard][value] = "Stand"
            elif (temp == soft_hit_expected_values[upcard][value]):
                soft_optimal_moves[upcard][value] = "Hit"
            else:
                soft_optimal_moves[upcard][value] = "DD"
    return pd.DataFrame(soft_optimal_moves)

def create_split_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of the expected values for splitting.

    :param dealer_upcards: List of dealer upcard values.
    :return: Dictionary mapping each upcard to its optimal expected value for splits.
    """
    split_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        split_dict[upcard] = split_EV(upcard_value)
    return split_dict

def create_split_EV_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_split_EV_dict(dealer_upcards))

def create_split_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    optimal_dict = create_optimal_dict(dealer_upcards)
    split_dict = create_split_EV_dict(dealer_upcards)
    final_dict = {}
    for upcard in dealer_upcards:
        final_dict[upcard] = {}
        for i in range(2, 12):
            if split_dict[upcard][i] > (optimal_dict[upcard][i*2] if i != 11 else optimal_dict[upcard][i]):
                final_dict[upcard][i] = "S"
            else:
                final_dict[upcard][i] = "_"
    return pd.DataFrame(final_dict)
                