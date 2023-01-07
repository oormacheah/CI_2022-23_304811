from nim import *

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]
    # Iterator may be exhausted if no possible move gives 0 nim-sum, so that you would pick at random

# Task 3.1 - Fixed rules
def my_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    if all(r <= 1 for r in state.rows):
        return (random.choice(data["brute_force"]))[0]
    next_active_row = next(r for r, o in data["sorted_rows"] if o > 1)

    if data["active_rows_number"] % 2 == 0:
        # If number of rows is even, take all except 1 or take as many as possible from the shortest row 
        # (bigger than 1)
        if state.k is None or state.rows[next_active_row] <= state.k + 1:
            return Nimply(next_active_row, state.rows[next_active_row] - 1) # Remove all except one
    else:
        # If number of rows is odd, try to take all or as many as possible from the shortest row
        if state.k is None or state.rows[next_active_row] <= state.k:
            return Nimply(next_active_row, state.rows[next_active_row]) # Remove all except one

    # If there is a k and you got more than k + 1 or k
    return Nimply(next_active_row, state.k) # Subtract the max k allowed

# Task 3.2 - Evolvable strategy
def make_strategy(genome: dict) -> Callable:

    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if random.random() < genome["p"]:
            ply = Nimply(data["shortest_row"], random.randint(1, state.rows[data["shortest_row"]]))
        else:
            ply = Nimply(data["longest_row"], random.randint(1, state.rows[data["longest_row"]]))

        return ply

    return evolvable