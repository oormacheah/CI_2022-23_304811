import numpy as np
import random
from nim import *

class Agent(object):
    def __init__(self, state: Nim, alpha=0.15, random_factor=0.2, discount=0.4):
        self.state_action_history = []  # [(state, reward)]
        self.alpha = alpha
        self.random_factor = random_factor
        self.discount_factor = discount
        self.Q = {}
        self.init_reward(state)

    def init_reward(self, state: Nim):
        # Initialize reward for state, action pairs (Q-table)
        for s in state.possible_states():
            self.Q[s] = {}
            for m in possible_moves_external(s, state.k):
                self.Q[s][m] = 0 # np.random.uniform(low=0.1, high=1.0)

    def choose_action(self, state, allowedMoves, evaluation=False):
        maxQ = -10e15
        next_move = None
        randomN = random.random()
        if randomN < self.random_factor and not evaluation:
            # if random number below random factor, choose random action
            next_move = random.choice(allowedMoves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest Q value (reward)
            for action in allowedMoves:
                # new_state = nimming_new_obj(state, action)
                # print(new_state)
                # print(self.Q[new_state])
                if self.Q[state][action] >= maxQ:
                    next_move = action
                    maxQ = self.Q[state][action]

        return next_move

    def update_state_history(self, state, action, reward):
        self.state_action_history.append((state, action, reward))

    def change_state_history(self, state, action, reward):
        self.state_action_history[-1] = (state, action, reward)

    def learn(self):
        # target = 1
        # exit()
        for i in range(len(self.state_action_history) - 1):
            st, act, reward = self.state_action_history[i]
            new_st, _, _ = self.state_action_history[i + 1]
            self.Q[st][act] += self.alpha * (reward + self.discount_factor * max(self.Q[new_st].values()) - self.Q[st][act])
            # target += reward

        # Add the missing part of the puzzleù
        i += 1
        st, act, reward = self.state_action_history[i]
        self.Q[st][act] += self.alpha * (reward - self.Q[st][act])

        self.state_action_history = []

        # self.random_factor -= 10e-5  # decrease random factor each episode of play

    def ply(self, state: Nim) -> Nimply:
        return self.choose_action(state, state.allowed_states[state.rows], evaluation=True)
