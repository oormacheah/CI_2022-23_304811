from nim import *
from strategies import *

logging.getLogger().setLevel(logging.INFO)

# single_match(my_strategy, gabriele)

print(single_match(make_strategy({'p': 0.7}), pure_random, 10))

# Fixed strategy
# print(evaluate(my_strategy, optimal_strategy, 500, 4))

# Sequence of "training" matches


