# Chapter 18 - Reinforcement Learning

## Basic Concept
- An agent makes observations and takes actions within an environment, and in return receives rewards.
- There can be positive and/or negative rewards.
- Policy: the algorithm the agent uses to determine its actions
- Methods to search the policy space
    - Brute force: try all possible combinations of parameters
    - Genetic
    - Neural Network

## Tools to create Environment
- PyBullet
- MuJoCo
- OpenAI Gym
- TF-Agents Library (Google)
- DM Control library (DeepMind)

## Credit Assignment Problem
- It is hard to know which action is responsible for the rewards.
- Solution: evaluate an action based on the sum of all the rewards that come after it, usually applying a discount factor gamma at each step.
- Action's return: sum of discounted rewards
- Run many episodes and normalize the actions' returns across all actions -> Action Advantage for each action

## Policy Gradients
- Reward is a function of actions, and action is a function of policy parameters.
- Policy gradient: The gradient of the rewards with regard to the policy parameters
- The reward needs to be maximized.

## REINFORCE algorithm
- Algorithm
    1. Let the neural network play the game several times.
        - At each step, compute the gradients of the reward regards to model parameters that would make the chosen action even more likely. Save the gradients but do not apply them yet.
    2. Compute each action's advantages once some episodes are finished.
    3. Multiply the action's advantages with each gradient vector so the gradient are adjusted based on the advantages.
    4. Compute the mean of all the resulting gradient vectors and perform gradient ascent step.

## Markov Decision Processes
- Markov Decision Processes: Markov chain with actions when transitioning states.
- Rewards are associated with the actions
- Given a known Markov Decision Processes
    - Optimal State Value (of a state s): sum of all discounted future rewards the agent can expect on average after it reaches a state s, assuming it acts optimally. It is a function of state s and discounted rate.
    - Q-Value (Quality Value): optimal Q-Value of a state-action pair (s,a) is the sum of discounted future rewards the agent can expect on average after it reaches the state s and chooses action a, but before it sees the outcome fo this action, assuming it acts optimally after that action. It is a function of state s, action a, and the discounted rate.

## Learning the paramters of a Markov Decision Processes
- The transition probabilities and the rewards are not known in advance.
- Algorithms
    - Temporal Difference Learning (TD-Learning): Run a random policy to iteratively update the estimation of transition probabilities and rewards.
    - Q-Learning: run some policy (maybe random) to estimate the optimal Q-Value for each state-action pair.
        - Off-policy algorithm: the exploration policy used in the training (random) is not the policy that will be used.
        - Alternative exploration policy to pure random
            - esilon-greedy policy: at each step it have some probability p to act greedily by choosing the action that maximize the Q-Value or probability 1-p to act randomly
            - Change Q-value by adding a term encouraging exploring relative under-explored actions.

## Q-Learning at Scale
- Original Q-Learning algorithm is not good at scaling to large MDPs.
- Approximate Q-Learning: use a approximate function to estimate actual Q-value, for example, a linear combination of the states.
- Deep Q-Learning: using deep neural network to estimate Q-value
    - Fixed Q-Value Targets
    - Double DQN
    - Prioritized Experience Replay
    - Dueling DQN