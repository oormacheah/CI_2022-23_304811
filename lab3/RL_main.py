from nim import Nim
from RL_agent import Agent
from strategies import *
import matplotlib.pyplot as plt

NIM_SIZE = 4
k = None
alpha = 0.1
exploit_vs_explore = 0.2
opponent_strategy = optimal_strategy

if __name__ == '__main__':
    nim = Nim(NIM_SIZE, k, RL=True)
    robot = Agent(nim.possible_states(), alpha=alpha, random_factor=exploit_vs_explore)
    moveHistory = []
    indices = []

    print(nim)

    for i in range(5000):
        while not nim.is_game_over():
            state, _ = nim.get_state_and_reward(agent_playing=True)  # get the current state
            # choose an action (explore or exploit)
            action = robot.choose_action(state, nim.allowed_states[state])
            nim.nimming(action)  # update the nim according to the action
            state, reward = nim.get_state_and_reward(agent_playing=False)  # get the new state and reward
            # update the robot memory with state and reward
            robot.update_state_history(state, reward)
            if nim.steps > 1000:
                # end the robot if it takes too long to find the goal
                nim.robot_position = (5, 5)
        robot.learn()  # robot should learn after every episode
        # get a history of number of steps taken to plot later
        if i % 50 == 0:
            print(f"{i}: {nim.steps}")
            moveHistory.append(nim.steps)
            indices.append(i)
        nim = nim = Nim(NIM_SIZE, k, RL=True)  # reinitialize the board

plt.semilogy(indices, moveHistory, "b")
plt.show()
