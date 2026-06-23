import pandas as pd
from pyscript import display, HTML, when, web
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np
import random
import math
import more_itertools
import itertools
import ast

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
        

def findMorePopular(outcome1, outcomes, agentCoordinates, agentToRoomId1, agentToRoomId):
    result = []
    for i in range(len(outcomes)):
        if (len(N(outcome1, outcomes[i], agentCoordinates, agentToRoomId1, agentToRoomId[i])) <
            len(N(outcomes[i], outcome1, agentCoordinates, agentToRoomId[i],agentToRoomId1))):
            result.append(outcomes[i])
    return result

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

# Auxiliary functions

def generateOutcomeAgentDistanceTable(outcomes):
    outcomesAgentToRoomID = generateAgentsToRoomIdAllOutcomes(outcomes, range(settings["nrAgents"]))
    
    outcomeAgentDistanceTable = {}

    for i in range(len(outcomes)):
        outcomeAgentDistanceTable[i] = {}
        for j in range(settings["nrAgents"]):
            outcomeAgentDistanceTable[i][j] = distToRoom(outcomes[i], j, outcomesAgentToRoomID[i], settings["agentsCoordinates"])

    return outcomeAgentDistanceTable

def distanceAgentRoom(agent, room, agentCoordinates):
    dist = 0
    for a in room:
        dist += math.dist(agentCoordinates[agent], agentCoordinates[a])
    return dist

def agentRoomRank(agent, room, agentCoordinates):
    rank = 0
    agents = set(range(settings["nrAgents"]))
    rooms = [sublist for sublist in list(itertools.combinations(agents, settings["roomsize"])) if agent in sublist]
    roomdist = distanceAgentRoom(agent, room, agentCoordinates)
    
    for r in rooms:
        if distanceAgentRoom(agent, r, agentCoordinates) < roomdist:
            rank += 1
    return rank

def outcomeAgentRank(outcome, agent, agentCoordinates):
    room =  [sublist for sublist in outcome if agent in sublist][0]
    return agentRoomRank(agent, room, agentCoordinates)

def outcomeAgentsRank(outcome, agentCoordinates):
    result = []
    for agent in range(settings["nrAgents"]):
        result.append(outcomeAgentRank(outcome, agent, agentCoordinates))
    return result

def N_aux(outcome1, outcome2, agentCoordinates):
    result = []
    agents = range(settings["nrAgents"])
    for agent in agents:
        outcome1room = [sublist for sublist in outcome1 if agent in sublist][0]
        outcome2room = [sublist for sublist in outcome2 if agent in sublist][0]

        if distanceAgentRoom(agent, outcome1room, agentCoordinates) < distanceAgentRoom(agent, outcome2room, agentCoordinates):
            result.append(agent)

    return result


settings = {
    "initialized": False,

    "dimensions": 2,
    "maxCoordinates": [],
    "minCoordinates": [],
    "nrAgents": -1,
    "roomsize": -1,
    "nrRooms": -1,
    "agentsCoordinates": {},
    "valid": True,
    
    "already-computed": False,
    "outcomes": [],
    "outcomesAgentToRoomID": {},
    "popoutcomesids": []
}


@when("click", "#random-button")
def plot_input_random(event):
    """
    Plot input points
    """

    settings["initialized"] = True
    settings["already-computed"] = False
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

    df = pd.DataFrame.from_dict(settings["agentsCoordinates"], orient="index", columns=["x", "y"])
    df.index.name = "Agent"

    display(df, target="agent-coordinates-output", append=False)

    output = web.page["agent-coordinates-output-raw"]
    output.innerText = ""
    output.innerText = str(settings["agentsCoordinates"])

@when("click", "#manual-button")
def plot_input_manual(event):
    """
    Plot input points
    """
    settings["initialized"] = True
    settings["already-computed"] = False
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

    df = pd.DataFrame.from_dict(settings["agentsCoordinates"], orient="index", columns=["x", "y"])
    df.index.name = "Agent"

    display(df, target="agent-coordinates-output", append=False)
    
    output = web.page["agent-coordinates-output-raw"]
    output.innerText = ""
    output.innerText = str(settings["agentsCoordinates"])


@when("click", "#btn-plot")
def show_matplotlib_plot(event):
    """
    Display a single matplotlib plot.
    """
    if settings["initialized"]:
        if settings["valid"]:
            output = web.page["output-popular-outcomes-raw"]
            output.innerText = ""

            # Compute all possible outcomes and find the popular ones
            if not settings["already-computed"]:
                settings["outcomes"] = part(range(settings["nrAgents"]), settings["nrRooms"])
                settings["outcomesAgentToRoomID"] = generateAgentsToRoomIdAllOutcomes(settings["outcomes"], range(settings["nrAgents"]))
                settings["popoutcomesids"] = findPopularOutcomes(settings["outcomes"], settings["agentsCoordinates"], settings["outcomesAgentToRoomID"])
                settings["already-computed"] = True

            # Create the string for popular outcomes
            popoutcomes = []
            for i in settings["popoutcomesids"]:
                popoutcomes.append(settings["outcomes"][i])


            display(HTML("Popular Outcomes"),
                    target="plot-output", append=False)
            
            if is1d(settings["agentsCoordinates"]) and settings["roomsize"] == 2:
                for i in settings["popoutcomesids"]:
                    fig = plotOutcome1DCurve(settings["outcomes"][i], settings["agentsCoordinates"], settings["nrAgents"])
                    display(fig, target="plot-output")
                    plt.close(fig)
            else:
                for i in settings["popoutcomesids"]:
                    fig = plotOutcome(settings["outcomes"][i], settings["agentsCoordinates"], settings["nrAgents"])
                    display(fig, target="plot-output")
                    plt.close(fig)

            output_div = web.page["output-popular-outcomes"]
            if len(popoutcomes) == 0:
                output_div.innerText = "No popular outcomes"
            else:
                df = pd.DataFrame(
                    [[str(part) + ',' for part in partition[:-1]] + [str(partition[-1])] for partition in popoutcomes],
                    columns=[f"Room {i+1}" for i in range(len(popoutcomes[0]))]
                )
                df.index.name = "Outcome"
                display(df, target="output-popular-outcomes", append=False)


                output.innerText = "[" + ",\n".join(map(str, popoutcomes)) + "]"

    else:
        web.page["error-output"].innerText = "Roommate Game not initialized"


@when("click", "#find-morepop-button")
def find_more_popular_outcome(event):
    """
    Display a single matplotlib plot.
    """
    if settings["initialized"]:
        if settings["valid"]:
            output = web.page["more-popular-output-raw"]
            output.innerText = ""


            # Compute all possible outcomes and find the popular ones
            if not settings["already-computed"]:
                settings["outcomes"] = part(range(settings["nrAgents"]), settings["nrRooms"])
                settings["outcomesAgentToRoomID"] = generateAgentsToRoomIdAllOutcomes(settings["outcomes"], range(settings["nrAgents"]))
                settings["popoutcomesids"] = findPopularOutcomes(settings["outcomes"], settings["agentsCoordinates"], settings["outcomesAgentToRoomID"])
                settings["already-computed"] = True

            # Create the string for popular outcomes

            input_text = web.page["manual-outcome-more-popularinput"]
            test_outcome =  ast.literal_eval("\n".join(line.strip() for line in input_text.value.splitlines()))

            test_agent_to_roomID = generateAgentsToRoomIdAllOutcomes([test_outcome], range(settings["nrAgents"]))[0]
            morepopoutcomes = findMorePopular(test_outcome, settings["outcomes"], settings["agentsCoordinates"], test_agent_to_roomID, settings["outcomesAgentToRoomID"])


            display(HTML("More Popular Outcomes"),
                    target="more-popular-output", append=False)

            output_div = web.page["more-popular-output"]
            if len(morepopoutcomes) == 0:
                output_div.innerText = "Input outcome is popular"
            else:
                df = pd.DataFrame(
                    [[str(part) + ',' for part in partition[:-1]] + [str(partition[-1])] for partition in morepopoutcomes],
                    columns=[f"Room {i+1}" for i in range(len(morepopoutcomes[0]))]
                )
                df.index.name = "Outcome"
                display(df, target="more-popular-output", append=False)
                output.innerText = "[" + ",\n".join(map(str, morepopoutcomes)) + "]"

    else:
        web.page["error-output"].innerText = "Roommate Game not initialized"


@when("click", "#manual-plot-button")
def show_manual_matplotlib_plot(event):
    if settings["initialized"]:

        display(HTML("Manually Inputted Outcomes"),
                target="manual-plot-output", append=False)
                
        input_text = web.page["manual-outcome-input"]

        manualOutcomes =  ast.literal_eval("\n".join(line.strip() for line in input_text.value.splitlines()))
        if is1d(settings["agentsCoordinates"]) and settings["roomsize"] == 2:
            for outcome in manualOutcomes:
                fig = plotOutcome1DCurve(outcome, settings["agentsCoordinates"], settings["nrAgents"])
                display(fig, target="manual-plot-output")
                plt.close(fig)
        else:
            for outcome in manualOutcomes:
                fig = plotOutcome(outcome, settings["agentsCoordinates"], settings["nrAgents"])
                display(fig, target="manual-plot-output")
                plt.close(fig)
    else:
        web.page["error-output"].innerText = "Roommate Game not initialized"


@when("click", "#manual-distance-button")
def show_distance_table(event):
    if settings["initialized"]:
                
        input_text = web.page["manual-outcome-input"]

        manualOutcomes =  ast.literal_eval("\n".join(line.strip() for line in input_text.value.splitlines()))
        raw_data = generateOutcomeAgentDistanceTable(manualOutcomes)

        df = pd.DataFrame.from_dict(raw_data, orient="index")
        df.index.name = "Outcome"
        df.columns = [f"Agent {i}" for i in df.columns]
        display(df, target="manual-distance-output", append=False)
    else:
        web.page["error-output"].innerText = "Roommate Game not initialized"





@when("click", "#manual-rank-button")
def show_rank_table(event):
    if settings["initialized"]:
                
        input_text = web.page["manual-outcome-input"]

        manualOutcomes =  ast.literal_eval("\n".join(line.strip() for line in input_text.value.splitlines()))
        raw_data = []
        
        for outcome in manualOutcomes:
            raw_data.append(outcomeAgentsRank(outcome, settings["agentsCoordinates"]))

        df = pd.DataFrame(raw_data)
        df.index.name = "Outcome"
        df.columns = [f"Agent {i}" for i in df.columns]
        display(df, target="manual-rank-output", append=False)
    else:
        web.page["error-output"].innerText = "Roommate Game not initialized"





@when("click", "#popularity-margin-button")
def show_popmargin(event):
    if settings["initialized"]:
        output = web.page["popularity-margin-output"]
        output.innerText = ""

        input_text1 = web.page["popmargin-outcome1-input"]
        input_text2 = web.page["popmargin-outcome2-input"]

        outcome1 =  ast.literal_eval("\n".join(line.strip() for line in input_text1.value.splitlines()))
        outcome2 =  ast.literal_eval("\n".join(line.strip() for line in input_text2.value.splitlines()))
        
        popmargin = N_aux(outcome1, outcome2, settings["agentsCoordinates"])

        output.innerText = str(popmargin)

    else:
        web.page["error-output"].innerText = "Roommate Game not initialized"