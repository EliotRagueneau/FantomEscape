## implementation chaine de markov

import numpy as np
import random as rm

def begin():
    states = ["room","couloir","intersection"]
    transitionName = [["rc","ri"],["ci","cr","cc"],["ir","ic","ii"]] ## possibles events
    matrix_trans=[[0.5,0.5],[0.4,0.5,0.1],[0.5,0.4,0.1]] ## proba of each events
    begingame= rm.choice(states) ## on arrangera quand je vais completer les etats
    activite_list=[begingame]
    for line in range(0,3):
        for column in range(0,3):
            matrix=9*[9*[]]
            prob = 1
            print("begingame "+ begingame )
            if begingame == "room":
                change = np.random.choice(transitionName[0],replace=True,p=matrix_trans[0])
                if change == "rc":
                    prob = prob * 0.5
                    activite_list.append("couloir")
                elif change == "ri":
                    prob = prob * 0.5
                    activite_list.append("intersection")
            if begingame == "couloir":
                change= np.random.choice(transitionName[1],replace=True,p=matrix_trans[1])
                if change == "ci":
                    prob=prob * 0.4
                    activite_list.append("intersection")
                elif change == "cr":
                    prob=prob * 0.5
                    activite_list.append("room")
                elif change == "cc":
                    prob=prob * 0.1
                    activite_list.append("couloir")
            if begingame == "intersection":
                change= np.random.choice(transitionName[2],replace=True,p=matrix_trans[2])
                if change == "ir":
                    prob=prob * 0.5
                    activite_list.append("room")
                elif change == "ic":
                    prob=prob * 0.4
                    activite_list.append("couloir")
                elif change == "ii":
                    prob=prob * 0.1
                    activite_list.append("intersection")

            begingame=activite_list[column]
            print("Possible states: "+ str(activite_list))
            print("Probability of the possible sequence of states: " + str(prob))
        matrix[0]=(activite_list)
        matrix[1]=(activite_list)
        matrix[2]=(activite_list)
        matrix[3]=(activite_list)
        matrix[4]=(activite_list)
        matrix[5]=(activite_list)
        matrix[6]=(activite_list)
        matrix[7]=(activite_list)
        matrix[8]=(activite_list)
        for line in matrix:
            print(line)
begin()
