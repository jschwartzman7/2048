from agents.basicagents import Agent, Priority, Random
import agents.searchagents as sa
import agents.montecarloagents as ma
import agents.montecarloagents as ma
import game.boardnodes as nodes
from game.gameboard import moveDown, moveUp, randomTestBoardWeighted, randomStartingBoard, log2Board
import utils as utils
from utils import testBoards
import boardevaluation.evaluationfunctions as ef
import game.simulations as sims
import numpy as np
from scoring import testBasicAgents, testSearchAgents, testMonteCarloAgents, testAllAgents, testAgents, displayAssessAgents
import pygame as pg
from pyGame.display import UserPlay2048, Display, Modes, EvaluationAnalysis, GameTree
import agents.mlagents as ml
import tests.boardmanipulationTests as boardTests


def main():
    agent = ma.MCTSAgent()
    print(sims.simulateGame(agent))
    


if __name__ == "__main__":
    main()