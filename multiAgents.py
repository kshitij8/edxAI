# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    food=[]
    for i in newFood.asList():
    	food.append(manhattanDistance(newPos,i))
    score=0
    if len(food)>0 :
    	score=1/sum(food)+5/min(food)+successorGameState.getScore()
    if action=='Stop':
    	return score/10
    for i in newGhostStates:
    	if manhattanDistance(newPos,i.getPosition())<2:
    		return -10
    if score>0:
    	return score
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def value(self,gameState,depth,agent):
  	#print "depth",depth
  	if depth==0 or gameState.isWin() or gameState.isLose():
  		return (self.evaluationFunction(gameState),None)
  	if agent>=gameState.getNumAgents():
  		agent=agent%gameState.getNumAgents()
  		depth-=1
  	if agent==0:
  		return self.maxi(gameState,depth,agent)
  	else:
  		return self.mini(gameState,depth,agent)
  def maxi(self,gameState,depth,agent):
  	v=float('-inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1)[0]
  		if tem>v:
  			v=tem
  			act=i
  	#print v
  	return (v,act)
  def mini(self,gameState,depth,agent):
  	v=float('inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1)[0]
  		if tem<v:
  			v=tem
  			act=i
  	#print v
  	return (v,act)
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    ans=self.value(gameState,self.depth,0)
    #print ans[0],"depth",self.depth
    return ans[1]
    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def value(self,gameState,depth,agent,alpha,beta):
	#print "depth",depth
	if depth==0 or gameState.isWin() or gameState.isLose():
		return (self.evaluationFunction(gameState),None,alpha,beta)
	if agent>=gameState.getNumAgents():
		agent=agent%gameState.getNumAgents()
		depth-=1
  	if agent==0:
  		return self.maxi(gameState,depth,agent,alpha,beta)
  	else:
  		return self.mini(gameState,depth,agent,alpha,beta)
  def maxi(self,gameState,depth,agent,alpha,beta):
  	v=float('-inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if v>beta:
  			break
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1,alpha,beta)
  		alpha=tem[2]
  		beta=tem[3]
  		tem=tem[0]
  		if tem>v:
  			v=tem
  			act=i
  	#print v
  	return (v,act,alpha,v)
  def mini(self,gameState,depth,agent,alpha,beta):
  	v=float('inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if v<alpha:
  			break
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1,alpha,beta)
  		alpha=tem[2]
  		beta=tem[3]
  		tem=tem[0]
  		if tem<v:
  			v=tem
  			act=i
  	#print v
  	return (v,act,v,beta)
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    ans=self.value(gameState,self.depth,0,float("-inf"),float("+inf"))
    #print ans[0]
    return ans[1]
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def value(self,gameState,depth,agent):
	#print "depth",depth
	if depth==0 or gameState.isWin() or gameState.isLose():
		return (self.evaluationFunction(gameState),None)
	if agent>=gameState.getNumAgents():
		agent=agent%gameState.getNumAgents()
		depth-=1
  	if agent==0:
  		return self.maxi(gameState,depth,agent)
  	else:
  		return self.expecti(gameState,depth,agent)
  def maxi(self,gameState,depth,agent):
  	v=float('-inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1)[0]
  		if tem>v:
  			v=tem
  			act=i
  	#print v
  	return (v,act)
  def expecti(self,gameState,depth,agent):
  	v=0
  	act=None
  	acts=gameState.getLegalActions(agent)
  	act=random.choice(acts)
  	#v=self.value(gameState.generateSuccessor(agent,act),depth,agent+1)[0]
  	#return (self.evaluationFunction(gameState),random.choice(acts))
  	for i in acts:
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1)[0]
  		v=v+tem/5.0
  		#if tem<v:
  			#v=tem
  		act=i
  	#print v
  	return (v,act)
  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    ans=self.value(gameState,self.depth-1,0)
    #print ans[0]
    return ans[1]
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
    Considered the inverse of the shortest distance to the nearest food
    If any ghost was within 1 block distance rated that state as bad,
    given the ghost wasn't scared
    Also, considered the inverse of sum of distance to food, to ensure pacman didnt 
    didn't venture too far off from remainder of food in pursuit of just one.'
    <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  Pos = currentGameState.getPacmanPosition()
  Food = currentGameState.getFood()
  GhostStates = currentGameState.getGhostStates()
  ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
  #print ScaredTimes
  food=[]
  for i in Food.asList():
	food.append(manhattanDistance(Pos,i))
  score=0
  if len(food)>0 :
  	score=1/sum(food)+5/min(food)+currentGameState.getScore()
  #ghost=0
  for i in GhostStates:
  	#ghost+=manhattanDistance(Pos,i.getPosition())
  	if i.scaredTimer==0 and manhattanDistance(Pos,i.getPosition())<2:
  		return 0
  #if ghost<5:
  	#return 0
  if score>0:
  	return score
  return currentGameState.getScore()
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    ans=self.value(gameState,self.depth,0,float("-inf"),float("+inf"))
    #print ans[0]
    return ans[1]
    util.raiseNotDefined()
  def evaluationFunction(gameState):
  	Pos = currentGameState.getPacmanPosition()
  	Food = currentGameState.getFood()
  	GhostStates = currentGameState.getGhostStates()
  	ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
  	#print ScaredTimes
  	food=[]
  	for i in Food.asList():
  		food.append(manhattanDistance(Pos,i))
  	score=0
  	if len(food)>0 :
  		score=1/sum(food)+5/min(food)+currentGameState.getScore()
  	#ghost=0
  	for i in GhostStates:
  	#ghost+=manhattanDistance(Pos,i.getPosition())
  		if i.scaredTimer==0 and manhattanDistance(Pos,i.getPosition())<2:
  			return 0
  	#if ghost<5:
  	#return 0
  	if score>0:
  		return score
  	return currentGameState.getScore()
  	util.raiseNotDefined()
  def value(self,gameState,depth,agent,alpha,beta):
  	#print "depth",depth
  	if depth==0 or gameState.isWin() or gameState.isLose():
  		return (self.evaluationFunction(gameState),None,alpha,beta)
  	if agent>=gameState.getNumAgents():
  		agent=agent%gameState.getNumAgents()
  		depth-=1
    	if agent==0:
    		return self.maxi(gameState,depth,agent,alpha,beta)
    	else:
    		return self.mini(gameState,depth,agent,alpha,beta)
  def maxi(self,gameState,depth,agent,alpha,beta):
  	v=float('-inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if v>beta:
  			break
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1,alpha,beta)
  		alpha=tem[2]
  		beta=tem[3]
  		tem=tem[0]
  		if tem>v:
  			v=tem
  			act=i
  	#print v
  	return (v,act,alpha,v)
  def mini(self,gameState,depth,agent,alpha,beta):
  	v=float('inf')
  	act=None
  	acts=gameState.getLegalActions(agent)
  	for i in acts:
  		if v<alpha:
  			break
  		if i=='Stop':
  			continue
  		tem=self.value(gameState.generateSuccessor(agent,i),depth,agent+1,alpha,beta)
  		alpha=tem[2]
  		beta=tem[3]
  		tem=tem[0]
  		if tem<v:
  			v=tem
  			act=i
  	#print v
  	return (v,act,v,beta)

