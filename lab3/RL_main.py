from nim import Nim
from RL_agent import Agent
from strategies import *
import matplotlib.pyplot as plt

NIM_SIZE = 3
k = None
alpha = 0.3
exploit_vs_explore = 0.2
discount_factor = 0.6
opponent_strategy = my_fixed_strategy
n_episodes = 5000

def train(NIM_SIZE, k, alpha, exploit_vs_explore, n_episodes):
    state = Nim(NIM_SIZE, k, RL=True)
    bot = Agent(state, alpha=alpha, random_factor=exploit_vs_explore, discount=discount_factor)
    indices = []
    action = None

    print(state)

    for i in range(n_episodes):

        player = 0
        prev = {0: {"state": None, "action": None}, 1: {"state": None, "action": None}} # Keep track of last state and action from each player

        while True:
            # state, _ = nim.get_state_and_reward(agent_playing=True)  # get the current state
            # choose an action (explore or exploit)

            action = bot.choose_action(state, state.allowed_states[state.rows])

            prev[player]["state"] = deepcopy(state)
            prev[player]["action"] = deepcopy(action)

            state.nimming(action)  # update the nim according to the action
            # print(f'Player {player} plays: {action}\n(equivalent) Board: {state}')

            if state.is_game_over():
                # update the robot memory with state and reward for the winner and for the losing move 
                reward = prev[1 - player]["state"].get_reward(winner=False)
                bot.change_state_history(prev[1 - player]["state"].rows, prev[1 - player]["action"], reward)

                reward = state.get_reward(winner=True)
                bot.update_state_history(prev[player]["state"].rows, action, reward)

                break
            else:
                reward = state.get_reward(winner=None)
                bot.update_state_history(prev[player]["state"].rows, action, reward)

            player = 1 - player

        bot.learn()  # robot should learn after every episode

        # get a history of number of steps taken to plot later
        # if i % 50 == 0:
        #     print(f"{i}: {nim.steps}")
        #     moveHistory.append(nim.steps)
        #     indices.append(i)
        state = Nim(NIM_SIZE, k, RL=True)  # reinitialize the board

    for k in sorted(bot.Q.keys()):
        print(k)
        for k1 in bot.Q[k]:
            print(k1, bot.Q[k][k1])
        print('\n')

    return bot

# plt.semilogy(indices, moveHistory, "b")
# plt.show()

if __name__ == '__main__':
    llamabot = train(NIM_SIZE, k, alpha, exploit_vs_explore, n_episodes)
    print(llamabot.random_factor)
    # nim = Nim(NIM_SIZE, k, RL=True)
    print(evaluate(llamabot.ply, opponent_strategy, 1000, NIM_SIZE, k, True))
