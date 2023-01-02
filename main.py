'''
Created on 17 Apr 2019

@author: rainman
'''
import json;
import random;
from scipy.stats import norm;
import math

def getGoals(team):
    matches = sum(team["xGoalGames"])
    px = []
    pxMu = []
    c = 0.0
    for x in team["xGoalGames"]:
        p = float(x / matches)
        px.append(float(p * c))
        c += 1
    mu = float(sum(px))
    c = 0.0
    for x in team["xGoalGames"]:
        p = float(x / matches)
        pxMu.append(float(p * pow((c - mu), 2)))
        c += 1
    sig = float(math.sqrt(float(sum(pxMu))))
    
    randomFloat = float(random.uniform(0, 1))
    goals = 0
    psum = 0.0
    j = 0.0
    for i in range(0, len(team["xGoalGames"])):
        psum = psum + norm.pdf(i, mu, sig)
        if(randomFloat <= psum and randomFloat > j):
            goals = i
            break
    return goals
    

def play_match(team1, team2):
    goals1 = getGoals(team1[1])
    goals2 = getGoals(team2[1])
        
    team1[1]["goalsFor"] += goals1
    team1[1]["goalsAgainst"] += goals2
    
    team2[1]["goalsFor"] += goals2
    team2[1]["goalsAgainst"] += goals1
    
    team1[1]["matchesPlayed"] += 1
    team2[1]["matchesPlayed"] += 1
    
    if(goals1 > goals2):
        team1[1]["wins"] += 1
        team1[1]["points"] += 3
        team2[1]["losses"] += 1
    if(goals1 < goals2):
        team2[1]["wins"] += 1
        team2[1]["points"] += 3
        team1[1]["losses"] += 1
    if(goals1 == goals2):
        team1[1]["points"] += 1
        team2[1]["points"] += 1

def main():
    with open('./teams.json', 'r') as data:
        teams = json.load(data)
    for team1 in teams.items():
        for team2 in teams.items():
            if(team1 != team2):
                play_match(team1, team2)
    standings = sorted(teams.items(), key=lambda k: (k[1].get('points'), float(k[1].get('goalsFor') / k[1].get('goalsAgainst'))), reverse=True)
    s = 1
    for standing in standings:
        print(str(s) +'.' + standing[0] + ": " + str(standing[1]["points"]) + " " + 
                                       str(standing[1]["wins"]) + "W-" + str(standing[1]["matchesPlayed"] - 
                                        standing[1]["wins"] - standing[1]["losses"]) + 
                                       "D-" + str(standing[1]["losses"]) + "L-" + str(standing[1]["goalsFor"]) + "GF-" + 
                                       str(standing[1]["goalsAgainst"])+ "GA")
        s += 1


main()
