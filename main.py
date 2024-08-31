from TableCreation import *
from MonteCarlo import *
dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
print(pd.DataFrame(create_stand_EV_dict(dealer_upcards)))
print(monte_carlo_stand(1000000, 14, 8))