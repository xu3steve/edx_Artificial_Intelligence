  # valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        """
        print mdp.getStates() #['TERMINAL_STATE', (0, 0), (0, 1), (0, 2)]
        print mdp.getPossibleActions((0, 1)) #('north', 'west', 'south', 'east')
        print mdp.getTransitionStatesAndProbs((0, 1), 'south') #[((0, 1), 0.0), ((0, 0), 1.0)]
        print mdp.getReward((0, 1), 'south', (0, 0)) # 0.0
        print mdp.getReward((0, 0), 'exit', 'TERMINAL_STATE') # 10
        print mdp.isTerminal('TERMINAL_STATE')  # True
        """
        #symbolic version
        #  for range 0 to iterations{
        #    foreach S in mdp.getStates(){
        #      V*(s) = max_a Q*(s,a)
        #      Q*(s,a) = E_s' T(s,a,s')[R(s,a,s') + gV*(s')]
        #    }
        #  }
         
          #code version
        #print self.values
          
        for _ in range(0,iterations):         
          newVals = util.Counter()        
          for s in mdp.getStates():    
            #print s     
            qvals = []
            for a in mdp.getPossibleActions(s):                          
              qvals.append(self.computeQValueFromValues(s, a)) 
            if len(qvals) > 0:
              #print qvals
              newVals[s] = max(qvals)
            else:
              newVals[s] = 0
          self.values = newVals;
          
        #print self.values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
          return 0
        
        
        actionval = 0
        for T in self.mdp.getTransitionStatesAndProbs(state,action):
          sprime = T[0]
          p = T[1]
          actionval += p * (self.mdp.getReward(state, action, sprime) + (self.discount * self.values[sprime]))
        
        return actionval; 

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        action = None
        bestv = float("-inf")
        for a in self.mdp.getPossibleActions(state):
          qv = self.computeQValueFromValues(state, a)
          if  qv > bestv:
            bestv = qv
            action = a
            
        return action
            

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
