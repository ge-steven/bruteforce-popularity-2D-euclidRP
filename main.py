from pyscript import display, HTML, when, web
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np
import random
import math
from itertools import combinations
import more_itertools
import ast
import textwrap
import js

# Computation functions
def generateAgents(dimensions, n):
    agents = {}
    coordinates_collection = []
    for i in range(n):
        coordinates = []
        for j in range(dimensions):
            coordinate = random.random() * (settings["maxCoordinates"][j] - settings["minCoordinates"][j]) + settings["minCoordinates"][j]
            coordinates.append(coordinate)
        coordinates_collection.append(coordinates)

    coordinates_collection.sort()
    for i in range(n):
        agents[i] = coordinates_collection[i]
    return agents

def allRoomsEqualSize(outcome):
    for i in outcome:
        for j in outcome:
            if len(i) != len(j):
                return False
    return True

def part(agents, nrRooms):
    return [x for x in more_itertools.set_partitions(range(len(agents)), nrRooms) if allRoomsEqualSize(x)]
                
def findRoomId(outcome, agentId):
    for i in range(settings["nrRooms"]):
        if agentId in outcome[i]:
            return i
        
def generateAgentsToRoomId(outcome, agents):
    agentsToRoomId = {}
    for i in agents:
        agentsToRoomId[i] = findRoomId(outcome, i)
    return agentsToRoomId

def generateAgentsToRoomIdAllOutcomes(outcomes, agents):
    outcomesAgentsToRoomId = {}
    for i in range(len(outcomes)):
        outcomesAgentsToRoomId[i] = generateAgentsToRoomId(outcomes[i], agents)
    return outcomesAgentsToRoomId

def distToRoom(outcome, agent, agentToRoomId, agentCoordinates):
    dist = 0
    room = outcome[agentToRoomId[agent]]
    for a in room:
        dist += math.dist(agentCoordinates[agent], agentCoordinates[a])
    return dist

def distAgentToRoom(room, agent, agentCoordinates):
    dist = 0
    for a in room:
        dist += math.dist(agentCoordinates[agent], agentCoordinates[a])
    return dist

def N(outcome1, outcome2, agentCoordinates, agentToRoomId1, agentToRoomId2):
    result = []
    for i in range(len(agentCoordinates)):
        if (distToRoom(outcome1, i, agentToRoomId1, agentCoordinates) < 
            distToRoom(outcome2, i, agentToRoomId2, agentCoordinates)):
            result.append(i)
    return result

def isPopular(outcome1, outcomes, agentCoordinates, agentToRoomId1, agentToRoomId):
    for i in range(len(outcomes)):
        if (len(N(outcome1, outcomes[i], agentCoordinates, agentToRoomId1, agentToRoomId[i])) <
            len(N(outcomes[i], outcome1, agentCoordinates, agentToRoomId[i],agentToRoomId1))):
            return False
    return True
        

def findPopularOutcomes(outcomes, agentCoordinates, agentToRoomId):
    popularIds = []
    for i in range(len(outcomes)):
        if isPopular(outcomes[i], outcomes, agentCoordinates, agentToRoomId[i], agentToRoomId):
            popularIds.append(i)
    return popularIds

# Plotting functions
def add_quadratic_arc(ax, x1, x2, level=0, base_height=0.6, span_scale=0.08,
                      level_scale=0.9, color="tab:orange", lw=2.5, zorder=1):
    """
    Draw a quadratic Bezier arc between x1 and x2.
    """
    if x1 > x2:
        x1, x2 = x2, x1

    span = abs(x2 - x1)
    height = (base_height + span_scale * span) * (1 + level_scale * level)
    xm = (x1 + x2) / 2.0

    verts = [(x1, 0.0), (xm, height), (x2, 0.0)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
    path = Path(verts, codes)

    patch = PathPatch(
        path,
        facecolor="none",
        edgecolor=color,
        lw=lw,
        zorder=zorder,
        capstyle="round"
    )
    ax.add_patch(patch)

def plotPoints(agentsCoordinates, nrAgents):
    x, y = np.array(list(agentsCoordinates.values())).T

    fig, ax = plt.subplots()
    ax.scatter(x,y)

    for i in range(nrAgents):
        ax.annotate(str(i), (x[i], y[i]))

    return fig

def plotOutcome(outcome, agentsCoordinates, nrAgents):
    x, y = np.array(list(agentsCoordinates.values())).T

    fig, ax = plt.subplots()
    ax.scatter(x,y)

    for i in range(nrAgents):
        ax.annotate(str(i), (x[i], y[i]))
        
    for room in outcome:
        x = []
        y = []
        for a in room:
            x.append(agentsCoordinates[a][0])
            y.append(agentsCoordinates[a][1])

        if settings["roomsize"] > 2:
            x.append(agentsCoordinates[room[0]][0])
            y.append(agentsCoordinates[room[0]][1])
        plt.plot(x, y, 'ro-')

    return fig

def plotOutcome1DCurve(outcome, agentsCoordinates, nrAgents):
    x, y = np.array(list(agentsCoordinates.values())).T

    fig, ax = plt.subplots()
    ax.scatter(x,y)

    for i in range(nrAgents):
        ax.annotate(str(i), (x[i], y[i]))
        
    for room in outcome:
        x = []
        y = []
        
        if abs(room[0]-room[1]) == 1:
            for a in room:
                x.append(agentsCoordinates[a][0])
                y.append(agentsCoordinates[a][1])
        else:
            add_quadratic_arc(
                ax,
                agentsCoordinates[room[0]][0],
                agentsCoordinates[room[1]][0],
                level=abs(room[0]-room[1]),
                color="orange",
                lw=1,
                zorder=1,
            )
        
        plt.plot(x, y, 'ro-')

    return fig

def is1d(agentsCoordinates):
    for coord in agentsCoordinates.values():
        if coord[1] != 0:
            return False
    return True


settings = {
    "dimensions": 2,
    "maxCoordinates": [],
    "minCoordinates": [],
    "nrAgents": -1,
    "roomsize": -1,
    "nrRooms": -1,
    "agentsCoordinates": {},
    "valid": True
}


@when("click", "#random-button")
def plot_input_random(event):
    """
    Plot input points
    """
    web.page["error-output"].innerText = ""
    settings["valid"] = True
    settings["roomsize"] = int(web.page["room-size"].value)
    settings["nrAgents"] = int(web.page["number-of-agents"].value)
    if settings["nrAgents"] % settings["roomsize"] != 0:
        settings["valid"] = False
        display("Number of agents is not a multiple of the room size!", target="error-output")
        raise ValueError("Number of agents is not a multiple of the room size!")

    maxCoordinates = []
    maxCoordinates.append(int(web.page["max-x"].value))
    maxCoordinates.append(int(web.page["max-y"].value))
    settings["maxCoordinates"] = maxCoordinates

    minCoordinates = []
    minCoordinates.append(int(web.page["min-x"].value))
    minCoordinates.append(int(web.page["min-y"].value))
    settings["minCoordinates"] = minCoordinates
    
    settings["agentsCoordinates"] = generateAgents(settings["dimensions"], settings["nrAgents"])
    settings["nrRooms"] = int(settings["nrAgents"] / settings["roomsize"])

    fig = plotPoints(settings["agentsCoordinates"], settings["nrAgents"])
    display(HTML("points"),
            target="input-plot-output", append=False)
    # Natively render the Matplotlib figure.
    display(fig, target="input-plot-output")
    plt.close(fig)

    output_div = web.page["output"]
    output_div.innerText = settings["agentsCoordinates"]

@when("click", "#manual-button")
def plot_input_manual(event):
    """
    Plot input points
    """
    web.page["error-output"].innerText = ""
    settings["valid"] = True

    input_text = web.page["input"] 
    settings["agentsCoordinates"] = ast.literal_eval("\n".join(line.strip() for line in input_text.value.splitlines()))

    settings["roomsize"] = int(web.page["room-size"].value)
    settings["nrAgents"] = len(settings["agentsCoordinates"])
    if settings["nrAgents"] % settings["roomsize"] != 0:
        settings["valid"] = False
        display("Number of agents is not a multiple of the room size!", target="error-output")
        raise ValueError("Number of agents is not a multiple of the room size!")


    settings["nrRooms"] = int(settings["nrAgents"] / settings["roomsize"])

    fig = plotPoints(settings["agentsCoordinates"], settings["nrAgents"])
    display(HTML("points"),
            target="input-plot-output", append=False)
    # Natively render the Matplotlib figure.
    display(fig, target="input-plot-output")
    plt.close(fig)

    output_div = web.page["output"]
    output_div.innerText = settings["agentsCoordinates"]


@when("click", "#btn-plot")
def show_matplotlib_plot(event):
    """
    Display a single matplotlib plot.
    """
    if settings["valid"]:
        # Compute all possible outcomes and find the popular ones
        outcomes = part(range(settings["nrAgents"]), settings["nrRooms"])
        outcomesAgentToRoomID = generateAgentsToRoomIdAllOutcomes(outcomes, range(settings["nrAgents"]))
        popoutcomesids = findPopularOutcomes(outcomes, settings["agentsCoordinates"], outcomesAgentToRoomID)

        # Create the string for popular outcomes
        popoutcomesstring = ""
        for i in popoutcomesids:
            popoutcomesstring += str(outcomes[i]) + "\n"


        display(HTML("Popular Outcomes"),
                target="plot-output", append=False)
        
        if is1d(settings["agentsCoordinates"]) and settings["roomsize"] == 2:
            for i in popoutcomesids:
                fig = plotOutcome1DCurve(outcomes[i], settings["agentsCoordinates"], settings["nrAgents"])
                display(fig, target="plot-output")
                plt.close(fig)
        else:
            for i in popoutcomesids:
                fig = plotOutcome(outcomes[i], settings["agentsCoordinates"], settings["nrAgents"])
                display(fig, target="plot-output")
                plt.close(fig)

        output_div = web.page["output-popular-outcomes"]
        if len(popoutcomesstring) == 0:
            output_div.innerText = "No popular outcomes"
        else:
            output_div.innerText = popoutcomesstring