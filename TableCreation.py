from ProbabilityFunctions import *
import pandas as pd

def create_dealer_prob_dist_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a probability distribution table for the dealer's possible outcomes.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        pd.DataFrame: DataFrame representing the probability distribution of the dealer's outcomes.
    """
    # Calculate the probability distribution for the dealer
    prob_dist = probability_distribution()
    
    # Create DataFrame from the probability distribution
    prob_df = pd.DataFrame(list(prob_dist.items()), columns=['Outcome', 'Probability']).round(4)
    prob_df.set_index('Outcome', inplace=True)
    
    return prob_df.T

def create_dealer_prob_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary mapping each dealer upcard to its probability distribution.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        dict: Dictionary mapping each upcard to its probability distribution.
    """
    prob_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        prob_dict[upcard] = probability_distribution(upcard_value)
    
    return prob_dict

def create_stand_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary mapping each dealer upcard to its expected value when standing.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        dict: Dictionary mapping each upcard to its expected value when standing.
    """
    stand_ev_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        stand_ev_dict[upcard] = stand_EV(upcard_value)
    
    return stand_ev_dict

def create_hit_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary mapping each dealer upcard to its expected value when hitting.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        dict: Dictionary mapping each upcard to its expected value when hitting.
    """
    hit_ev_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        hit_ev_dict[upcard] = total_hit_EV(upcard_value)
    
    return hit_ev_dict

def create_soft_hit_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary mapping each dealer upcard to its expected value when hitting with a soft hand.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        dict: Dictionary mapping each upcard to its expected value when hitting with a soft hand.
    """
    soft_hit_ev_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        soft_hit_ev_dict[upcard] = soft_hit_EV(upcard_value)
    
    return soft_hit_ev_dict

def create_double_down_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary mapping each dealer upcard to its expected value when doubling down.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        dict: Dictionary mapping each upcard to its expected value when doubling down.
    """
    double_down_ev_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        double_down_ev_dict[upcard] = total_hit_EV(upcard_value, double_down=True)
    
    return double_down_ev_dict

def create_double_down_soft_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary mapping each dealer upcard to its expected value when doubling down with a soft hand.

    Args:
        dealer_upcards (list): List of dealer upcard values.

    Returns:
        dict: Dictionary mapping each upcard to its expected value when doubling down with a soft hand.
    """
    double_down_soft_ev_dict = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        double_down_soft_ev_dict[upcard] = soft_hit_EV(upcard_value, double_down=True)
    
    return double_down_soft_ev_dict


def create_optimal_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of optimal expected values for each dealer upcard.

    Args:
        dealer_upcards (list): List of dealer upcard values (must be between 2 and 11, inclusive).

    Returns:
        dict: A dictionary mapping each upcard to its optimal expected value for all player hand values.
    """
    stand_values = create_stand_EV_dict(dealer_upcards)
    hit_values = create_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_EV_dict(dealer_upcards)

    optimal_values = {}
    
    for upcard in dealer_upcards:
        optimal_values[upcard] = {}
        for value in range(21, 3, -1):
            optimal_values[upcard][value] = max(
                stand_values[upcard].get(value, 0),
                hit_values[upcard].get(value, 0),
                double_down_values[upcard].get(value, 0)
            )
        
        # Include the Blackjack case separately
        optimal_values[upcard]["BJ"] = stand_values[upcard].get("BJ", 0)

    return optimal_values

def create_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves (Stand, Hit, or Double Down) for each dealer upcard.

    Args:
        dealer_upcards (list): List of dealer upcard values (must be between 2 and 11, inclusive).

    Returns:
        pd.DataFrame: A DataFrame representing the optimal move for each player hand value and dealer upcard.
    """
    stand_values = create_stand_EV_dict(dealer_upcards)
    hit_values = create_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_EV_dict(dealer_upcards)

    optimal_moves = {}
    
    for upcard in dealer_upcards:
        optimal_moves[upcard] = {}
        for value in range(21, 3, -1):
            # Determine the best move for the current hand value
            max_value = max(
                stand_values[upcard].get(value, 0),
                hit_values[upcard].get(value, 0),
                double_down_values[upcard].get(value, 0)
            )
            
            if max_value == stand_values[upcard].get(value, 0):
                optimal_moves[upcard][value] = "Stand"
            elif max_value == hit_values[upcard].get(value, 0):
                optimal_moves[upcard][value] = "Hit"
            else:
                optimal_moves[upcard][value] = "DD"

    return pd.DataFrame(optimal_moves)

def create_soft_optimal_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of optimal expected values for soft hands for each dealer upcard.

    Args:
        dealer_upcards (list): List of dealer upcard values (must be between 2 and 11, inclusive).

    Returns:
        dict: A dictionary mapping each dealer upcard to its optimal expected value for soft hands.
    """
    stand_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_values = create_soft_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_soft_EV_dict(dealer_upcards)

    soft_optimal_values = {}
    
    for upcard in dealer_upcards:
        soft_optimal_values[upcard] = {"BJ": stand_values[upcard].get("BJ", 0)}
        for value in range(21, 11, -1):
            soft_optimal_values[upcard][value] = max(
                stand_values[upcard].get(value, 0),
                soft_hit_values[upcard].get(value, 0),
                double_down_values[upcard].get(value, 0)
            )
    
    return soft_optimal_values

def create_soft_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves (Stand, Hit, or Double Down) for soft hands for each dealer upcard.

    Args:
        dealer_upcards (list): List of dealer upcard values (must be between 2 and 11, inclusive).

    Returns:
        pd.DataFrame: A DataFrame representing the optimal move for soft hands based on dealer upcards and player hand values.
    """
    stand_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_values = create_soft_hit_EV_dict(dealer_upcards)
    double_down_values = create_double_down_soft_EV_dict(dealer_upcards)

    soft_optimal_moves = {}
    
    for upcard in dealer_upcards:
        soft_optimal_moves[upcard] = {}
        for value in range(21, 11, -1):
            # Determine the best move for the current hand value
            max_value = max(
                stand_values[upcard].get(value, 0),
                soft_hit_values[upcard].get(value, 0),
                double_down_values[upcard].get(value, 0)
            )
            
            if max_value == stand_values[upcard].get(value, 0):
                soft_optimal_moves[upcard][value] = "Stand"
            elif max_value == soft_hit_values[upcard].get(value, 0):
                soft_optimal_moves[upcard][value] = "Hit"
            else:
                soft_optimal_moves[upcard][value] = "DD"

    return pd.DataFrame(soft_optimal_moves)

def create_split_EV_dict(dealer_upcards: list) -> dict:
    """
    Create a dictionary of expected values for splitting pairs of cards for each dealer upcard.

    Args:
        dealer_upcards (list): List of dealer upcard values (must be between 2 and 11, inclusive).

    Returns:
        dict: A dictionary mapping each dealer upcard to its expected values for splitting pairs of cards.
    """
    split_values = {}
    
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        split_values[upcard] = split_EV(upcard_value)
    
    return split_values


def create_split_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    """
    Create a table of optimal moves for splitting pairs of cards for each dealer upcard.

    Args:
        dealer_upcards (list): List of dealer upcard values (must be between 2 and 11, inclusive).

    Returns:
        pd.DataFrame: A DataFrame representing the optimal move (Split or Not Split) for each pair of cards against each dealer upcard.
    """
    optimal_values = create_optimal_dict(dealer_upcards)
    split_values = create_split_EV_dict(dealer_upcards)
    
    split_optimal_moves = {}
    
    for upcard in dealer_upcards:
        split_optimal_moves[upcard] = {}
        for pair_value in range(2, 12):
            # Compare the split value to the optimal value of hitting or standing
            optimal_for_pair = optimal_values[upcard].get(pair_value * 2, 0) if pair_value != 11 else optimal_values[upcard].get(pair_value + 1, 0)
            
            if split_values[upcard].get(pair_value, 0) > optimal_for_pair:
                split_optimal_moves[upcard][pair_value] = "S"  # 'S' for Split
            else:
                split_optimal_moves[upcard][pair_value] = "_"  # '_' for Do not Split

    return pd.DataFrame(split_optimal_moves)

                