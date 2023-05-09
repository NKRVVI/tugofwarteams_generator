import random
from classes import InputProcessor
from classes import Player
import copy
import math


def fitness(teams, information):
    team_size = []
    team_score = []
    for i in range(information.num_teams):
        team_size.append(teams.count(i))
        team_score.append(sum([information.participants[j].value if teams[j] == i else 0 for j in range(len(teams))]))

    if max(team_size) - min(team_size) >= 2:
        return 0

    return (1 / (max(team_score) - min(team_score))) if max(team_score) != min(team_score) else float('inf')


def get_initial_teams(information):
    teams = []
    for i in range(len(information.participants)):
        teams.append(i % information.num_teams)
    return teams


def get_neighbours(teams):
    neighbours = []
    for participant1 in range(len(teams)):
        for j in range(participant1 + 1, len(teams)):
            new_neighbour = copy.deepcopy(teams)
            new_neighbour[participant1], new_neighbour[j] = new_neighbour[j], new_neighbour[participant1]
            neighbours.append(new_neighbour)
    return neighbours


comp_information = InputProcessor('tugofwarparticipants.xlsx', 4)
print(comp_information.participants)
initial_teams = current_teams = get_initial_teams(comp_information)
initial_temperature = current_temperature = 10
cooling_rate = 0.95
num_iterations = 1000

for i in range(num_iterations):
    current_temperature *= cooling_rate
    neighbours = get_neighbours(current_teams)
    fitness_scores = [fitness(neighbour, comp_information) for neighbour in neighbours]
    best_teams = fitness_scores.index(max(fitness_scores))
    best_fitness = max(fitness_scores)
    current_fitness = fitness(current_teams, comp_information)

    if best_fitness >= current_fitness:
        current_teams = best_teams
    else:
        probability = math.exp((best_fitness - current_fitness) / current_temperature)
        if random.random() <= probability:
            current_teams = best_teams

print(current_teams, 1/fitness(current_teams))
