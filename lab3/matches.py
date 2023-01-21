from nim import *
from strategies import *
from min_max_agent import *

logging.getLogger().setLevel(logging.DEBUG)

# single_match(my_strategy, gabriele)

# print(single_match(make_strategy({'p': 0.7}), pure_random, 10))

# Fixed strategy
# print(evaluate(my_strategy, optimal_strategy, 500, 4))
# min_max_strategy = minimax_strategy(depth=5)

single_match(optimal_strategy, optimal_strategy, 3)


