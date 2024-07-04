import pandas as pd

def probability_distribution(dealer_upcard = None) -> dict: 
    def backtracking(path: list, result: dict) -> None:
        # Handle the conversion of a soft ace (11) to a hard ace (1) if it prevents busting
        if 11 in path and sum(path) >= 22:
            path = path[:]
            path[path.index(11)] = 1

        # Calculate probabilities and update the result dictionary
        total = sum(path)
        if total >= 17:
            total_probability = 1
            start = 0 if dealer_upcard == None else 1
            for i in range(start, len(path)):
                total_probability *= (1/13) if path[i] != 10 else (4/13)
            if (len(path) == 2) and (10 in path) and (11 in path):
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
    result = {num : 0 for num in range(17, 22)}
    result["bust"] = 0
    result["BJ"] = 0

    # Start the backtracking process
    if dealer_upcard:
        backtracking([dealer_upcard], result)
    else:
        backtracking([], result)
    return result

def stand_EV(num: int) -> dict:
    probabilities = probability_distribution(num)
    stand_EV = {num : 0 for num in range(21, 3, -1)}
    stand_EV["BJ"] = 0
    for player in stand_EV.keys():
        if player == "BJ":
            for value, prob in probabilities.items():
                if (value != "BJ"):
                    stand_EV[player] += prob
            stand_EV[player] *= 1.5
        else:
            for value, prob in probabilities.items():
                if (value == "BJ"):
                    stand_EV[player] -= prob
                elif (value == "bust"):
                    stand_EV[player] += prob
                elif (value < player):
                    stand_EV[player] += prob
                elif (value > player):
                    stand_EV[player] -= prob
    return stand_EV

def hit_EV(num: int) -> dict:
    s_EV = stand_EV(num)
    hit_EV = {}
    for i in range(21, 3, -1):
        total = 0
        for j in range(1, 11):
            if i + j > 21:
                total += -1/13 if j != 10 else -4/13
            else:
                prob = max([hit_EV[i+j], s_EV[i+j]])
                total += 1/13 * prob if j != 10 else 4/13 * prob
        hit_EV[i] = total
    return hit_EV

def soft_hit_EV(num: int) -> dict:
    s_EV = stand_EV(num)
    h_EV = hit_EV(num)
    soft_hit_EV = {}
    for i in range(21, 11, -1):
        total = 0
        for j in range(1, 11):
            if i + j > 21:
                prob = max(h_EV[i+j-10], s_EV[i+j-10])
                total += 1/13 * prob if j != 10 else 4/13 * prob
            else:
                prob = max([soft_hit_EV[i+j], h_EV[i+j], s_EV[i+j]])
                total += 1/13 * prob if j != 10 else 4/13 * prob
        soft_hit_EV[i] = total
    return soft_hit_EV

 ######################################## Table Creation Functions ########################################

def create_dealer_prob_dist_table(dealer_upcards: list) -> pd.DataFrame:
    df_overall_probabilities = pd.DataFrame(probability_distribution().items(), columns=['Outcome', 'Probability']).round(4)
    df_overall_probabilities.set_index('Outcome', inplace=True)
    df_overall_probabilities = df_overall_probabilities.T
    return df_overall_probabilities

def create_dealer_prob_dict(dealer_upcards: list) -> dict:
    dealer_probabilities = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        dealer_probabilities[upcard] = probability_distribution(upcard_value)
    return dealer_probabilities

def create_dealer_prob_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_dealer_prob_dict(dealer_upcards))

def create_stand_EV_dict(dealer_upcards: list) -> dict:
    stand_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        stand_expected_values[upcard] = stand_EV(upcard_value)
    return stand_expected_values

def create_stand_EV_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_stand_EV_dict(dealer_upcards))

def create_hit_EV_dict(dealer_upcards: list) -> dict:
    hit_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        hit_expected_values[upcard] = hit_EV(upcard_value)
    return hit_expected_values

def create_hit_EV_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_hit_EV_dict(dealer_upcards))

def create_soft_hit_EV_dict(dealer_upcards: list) -> dict:
    soft_hit_expected_values = {}
    for upcard in dealer_upcards:
        upcard_value = 11 if upcard == 'A' else int(upcard)
        soft_hit_expected_values[upcard] = soft_hit_EV(upcard_value)
    return soft_hit_expected_values

def create_soft_hit_EV_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_soft_hit_EV_dict(dealer_upcards))

def create_optimal_dict(dealer_upcards: list) -> pd.DataFrame:
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    hit_expected_values = create_hit_EV_dict(dealer_upcards)
    optimal_expected_values = {}
    for upcard in dealer_upcards:
        optimal_expected_values[upcard] = {"BJ": stand_expected_values[upcard]["BJ"]}
        for i in range(21, 10, -1):
            optimal_expected_values[upcard][i] = max(stand_expected_values[upcard][i], hit_expected_values[upcard][i])
    return optimal_expected_values

def create_optimal_values_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_optimal_dict(dealer_upcards))

def create_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    hit_expected_values = create_hit_EV_dict(dealer_upcards)
    optimal_moves = {}
    for upcard in dealer_upcards:
        optimal_moves[upcard] = {}
        for i in range(21, 10, -1):
            optimal_moves[upcard][i] = "Stand" if stand_expected_values[upcard][i] > hit_expected_values[upcard][i] else "Hit"
    return pd.DataFrame(optimal_moves)

def create_soft_optimal_dict(dealer_upcards: list) -> dict:
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_expected_values = create_soft_hit_EV_dict(dealer_upcards)
    soft_optimal_expected_values = {}
    for upcard in dealer_upcards:
        soft_optimal_expected_values[upcard] = {"BJ": stand_expected_values[upcard]["BJ"]}
        for i in range(21, 11, -1):
            soft_optimal_expected_values[upcard][i] = max(stand_expected_values[upcard][i], soft_hit_expected_values[upcard][i])
    return soft_optimal_expected_values

def create_soft_optimal_values_table(dealer_upcards: list) -> pd.DataFrame:
    return pd.DataFrame(create_soft_optimal_dict(dealer_upcards))

def create_soft_optimal_table(dealer_upcards: list) -> pd.DataFrame:
    stand_expected_values = create_stand_EV_dict(dealer_upcards)
    soft_hit_expected_values = create_soft_hit_EV_dict(dealer_upcards)
    soft_optimal_moves = {}
    for upcard in dealer_upcards:
        soft_optimal_moves[upcard] = {}
        for i in range(21, 11, -1):
            soft_optimal_moves[upcard][i] = "Stand" if stand_expected_values[upcard][i] > soft_hit_expected_values[upcard][i] else "Hit"
    return pd.DataFrame(soft_optimal_moves)