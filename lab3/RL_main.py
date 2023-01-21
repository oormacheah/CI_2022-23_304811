from nim import Nim
from RL_agent import Agent
from strategies import *
import matplotlib.pyplot as plt
import shelve

NIM_SIZE = 4
k = None
alpha = 0.2 # Learning rate
exploit_vs_explore = 0.8 # High exploration is key for achieving good results
discount_factor = 1 # Also, seems that considering the future reward only is better

training_opponent = pure_random
test_opponent = optimal_strategy
n_episodes = 3000
n_test_matches = 100

stepSize = 50 # For status printing only

saveQtable = True # False for loading the Q-table
Q_table_path = './data/Q_table_x.data'

def train(NIM_SIZE, k, alpha, exploit_vs_explore, n_episodes, printStatus=False, printQ=False):
    state = Nim(NIM_SIZE, k, RL=True)
    bot = Agent(state, alpha=alpha, random_factor=exploit_vs_explore, discount=discount_factor)
    indices = []
    action = None
    win_count = 0

    for i in range(n_episodes):
        player = 0 # Setting starting player as the number 0 (default)
        bot_idx = random.choice((0, 1)) # Set the bot to play first or second randomly

        last_state = None
        last_action = None

        # Game loop
        while True:
            # state, _ = nim.get_state_and_reward(agent_playing=True)  # get the current state
            # choose an action (explore or exploit)
            if player == bot_idx:
                action = bot.choose_action(state, state.allowed_states[state.rows])

                # Save last state and action only if the bot is playing
                last_state = deepcopy(state)
                last_action = deepcopy(action)

                state.nimming(action)  # update the nim according to the action
            else:
                opponent_ply = training_opponent(state)
                state.nimming(opponent_ply)

            if state.is_game_over():
                if player == bot_idx:
                    # Bot won
                    reward = state.get_reward(winner=True)
                    bot.update_state_history(last_state.rows, action, reward)
                    win_count += 1
                else:
                    reward = last_state.get_reward(winner=False)
                    bot.change_state_history(last_state.rows, last_action, reward)
                break
            else:
                # If the game is not over, give 0 rewards
                if player == bot_idx:
                    reward = state.get_reward(winner=None)
                    bot.update_state_history(last_state.rows, action, reward)
            player = 1 - player

        bot.learn()  # robot should learn after every episode

        # This print is used to keep track of the training and the win count (not very relevant)
        if printStatus:
            if i % stepSize == 0:
                print(f"{i}: Win count: {win_count}")
                # indices.append(i)
            state = Nim(NIM_SIZE, k, RL=True)  # reinitialize the board

    if printQ:
        for k in sorted(bot.Q.keys()):
            print(k)
            for k1 in bot.Q[k]:
                print(k1, bot.Q[k][k1])
            print('\n')

    if saveQtable:
        # Save table
        pass

    return bot

# plt.semilogy(indices, moveHistory, "b")
# plt.show()

if __name__ == '__main__':
    if saveQtable:
        llamabot = train(NIM_SIZE, k, alpha, exploit_vs_explore, n_episodes)
    else:
        # Load Q-table from Q_table_path
        pass

    win_rate = evaluate(llamabot.ply, test_opponent, n_test_matches, NIM_SIZE, k, True)
    print(f'Win rate against {test_opponent.__name__} (Bot playing FIRST): {round(win_rate * 100, 3)} %')
    win_rate = evaluate(test_opponent, llamabot.ply, n_test_matches, NIM_SIZE, k, True)
    print(f'Win rate against {test_opponent.__name__} (Bot playing SECOND): {round(win_rate * 100, 3)} %')
