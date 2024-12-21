# reactiveAgents.py
# ---------------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC
# Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
from ECTraining import train_all, decide


class NaiveAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        sense = state.getPacmanSensor()
        if sense[7]:
            action = Directions.STOP
        else:
            action = Directions.WEST
        return action


class PSAgent(Agent):
    "An agent that follows the boundary using production system."

    def getAction(self, state):
        sense = state.getPacmanSensor()
        x = [sense[1] or sense[2], sense[3] or sense[4],
             sense[5] or sense[6], sense[7] or sense[0]]
        if x[0] and not x[1]:
            action = Directions.EAST
        elif x[1] and not x[2]:
            action = Directions.SOUTH
        elif x[2] and not x[3]:
            action = Directions.WEST
        elif x[3] and not x[0]:
            action = Directions.NORTH
        else:
            action = Directions.NORTH
        return action


class ECAgent(Agent):
    "An agent that follows the boundary using error-correction."

    def registerInitialState(self, state):
        """Initialize the agent and train the perceptron weights."""
        labels = ['north', 'east', 'south', 'west']
        filenames = ['TrainingData/' + l + '.csv' for l in labels]

        # Train and get weights for each direction
        self.weight_sets = train_all(filenames)

        # Print the weights once after training
        for i, label in enumerate(labels):
            print(f"Weights for {label.upper()}: {self.weight_sets[i]}")

    def getAction(self, state):
        sense = state.getPacmanSensor()
        labels = ['north', 'east', 'south', 'west']

        # Make decisions based on trained weights
        decisions = []
        for i in range(len(labels)):
            decisions.append(decide(self.weight_sets[i], sense))

        # Return the direction based on the decision
        if decisions[0]:
            return Directions.NORTH
        elif decisions[1]:
            return Directions.EAST
        elif decisions[2]:
            return Directions.SOUTH
        elif decisions[3]:
            return Directions.WEST
        else:
            return Directions.NORTH


class SMAgent(Agent):
    "A sensory-impaired agent that follows the boundary using state machine."

    def registerInitialState(self, state):
        "The agent receives the initial GameState (defined in pacman.py)."
        sense = state.getPacmanImpairedSensor()  # Get the initial sensor readings
        self.prevAction = Directions.STOP  # Initialize with no movement
        self.prevSense = sense  # Store the initial sensor state

    def getAction(self, state):
        # Get the current sensory input (north, east, south, west)
        sense = state.getPacmanImpairedSensor()

        # Map sensor input (north, east, south, west)
        north_wall, east_wall, south_wall, west_wall = sense

        # The action that Pacman will take, based on the previous action and current sensors
        action = self.prevAction

        # If previous action was north and there's now a wall north, change direction
        if self.prevAction == Directions.NORTH and north_wall:
            if not east_wall:
                action = Directions.EAST
            elif not south_wall:
                action = Directions.SOUTH
            elif not west_wall:
                action = Directions.WEST
            else:
                action = Directions.STOP

        # If previous action was east and there's now a wall east, change direction
        elif self.prevAction == Directions.EAST and east_wall:
            if not south_wall:
                action = Directions.SOUTH
            elif not west_wall:
                action = Directions.WEST
            elif not north_wall:
                action = Directions.NORTH
            else:
                action = Directions.STOP

        # If previous action was south and there's now a wall south, change direction
        elif self.prevAction == Directions.SOUTH and south_wall:
            if not west_wall:
                action = Directions.WEST
            elif not north_wall:
                action = Directions.NORTH
            elif not east_wall:
                action = Directions.EAST
            else:
                action = Directions.STOP

        # If previous action was west and there's now a wall west, change direction
        elif self.prevAction == Directions.WEST and west_wall:
            if not north_wall:
                action = Directions.NORTH
            elif not east_wall:
                action = Directions.EAST
            elif not south_wall:
                action = Directions.SOUTH
            else:
                action = Directions.STOP

        # If no wall in the previous direction, continue moving in that direction
        if action == Directions.STOP:
            if not north_wall:
                action = Directions.NORTH
            elif not east_wall:
                action = Directions.EAST
            elif not south_wall:
                action = Directions.SOUTH
            elif not west_wall:
                action = Directions.WEST

        # Store the current sensory input and action for future reference
        self.prevSense = sense
        self.prevAction = action

        return action


