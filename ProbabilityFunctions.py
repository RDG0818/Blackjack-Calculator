def probability_distribution(dealer_upcard = None) -> dict: 
    def backtracking(path: list, result: dict):
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
                result["blackjack"] += total_probability
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
    result["blackjack"] = 0

    # Start the backtracking process
    if dealer_upcard:
        backtracking([dealer_upcard], result)
    else:
        backtracking([], result)
    return result

def stand_EV(num):
    probabilities = probability_distribution(num)
    stand_EV = {"blackjack" : 0, 21 : 0, 20 : 0, 19 : 0, 18 : 0, 17 : 0, "<=16" : 0}
    for player in stand_EV.keys():
        if player == "blackjack":
            for value, prob in probabilities.items():
                if (value != "blackjack"):
                    stand_EV[player] += prob
            stand_EV[player] *= 1.5
        elif player == "<=16":
            for value, prob in probabilities.items():
                if (value != "bust"):
                    stand_EV[player] -= prob
                else:
                    stand_EV[player] += prob
        else:
            for value, prob in probabilities.items():
                if (value == "blackjack"):
                    stand_EV[player] -= prob
                elif (value == "bust"):
                    stand_EV[player] += prob
                elif (value < player):
                    stand_EV[player] += prob
                elif (value > player):
                    stand_EV[player] -= prob
    return stand_EV

def hit_EV(num):
    stand_EV = stand_EV(num)
    hit_EV = {}
    for i in range(21, 10, -1):
        total = 0
        for j in range(1, 11):
            if i + j > 21:
                total += -1/13 if j != 10 else -4/13
            elif i + j > 16:
                prob = 0
                if (hit_EV[i+j] > stand_EV[i+j]):
                    prob = hit_EV[i+j]
                else:
                    prob = stand_EV[i+j]
                total += 1/13 * prob if j != 10 else 4/13 * prob
            else:
                prob = 0
                if (hit_EV[i+j] > stand_EV["<=16"]):
                    prob = hit_EV[i+j]
                else:
                    prob = stand_EV["<=16"]
                total += 1/13 * prob
        hit_EV[i] = total
    return hit_EV