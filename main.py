'''
Created on 17 Apr 2019

@author: rainman
'''
import json;
import random;
import matplotlib.mlab as mlab;
import math


def play_match(team1, team2):
    matches1 = sum(team1[1]["xGoalGames"])
    px1 = [];
    pxMu1 = [];
    c1 = 0.0;
    for x in team1[1]["xGoalGames"]:
        p = float(x / matches1);
        px1.append(float(p * c1));
        c1 += 1;
    mu1 = float(sum(px1));
    c1 = 0.0;
    for x in team1[1]["xGoalGames"]:
        p = float(x / matches1);
        pxMu1.append(float(p * pow((c1 - mu1), 2)))
        c1 += 1;
    sig1 = float(math.sqrt(float(sum(pxMu1))));
    
    random1 = float(random.uniform(0, 1));
    goals1 = 0;
    psum1 = 0.0;
    j1 = 0.0;
    for i in range(0, len(team1[1]["xGoalGames"])):
        psum1 = psum1 + mlab.normpdf(i, mu1, sig1);
        if(random1 <= psum1 and random1 > j1):
            goals1 = i;
            break;
    
    matches2 = sum(team2[1]["xGoalGames"])
    px2 = [];
    pxMu2 = [];
    c2 = 0.0;
    for x in team2[1]["xGoalGames"]:
        p = float(x / matches2);
        px2.append(float(p * c2));
        c2 += 1;
    mu2 = float(sum(px2));
    c2 = 0.0;
    for x in team2[1]["xGoalGames"]:
        p = float(x / matches2);
        pxMu2.append(float(p * pow((c2 - mu2), 2)))
        c2 += 1;
    sig2 = float(math.sqrt(float(sum(pxMu2))));
    
    random2 = float(random.uniform(0, 1));
    goals2 = 0;
    psum2 = 0.0;
    j2 = 0.0;
    for i in range(0, len(team2[1]["xGoalGames"])):
        psum2 = psum2 + mlab.normpdf(i, mu2, sig2);
        if(random2 <= psum2 and random2 > j2):
            goals2 = i;
            break;
        
    team1[1]["goalsFor"] += goals1;
    team1[1]["goalsAgainst"] += goals2;
    
    team2[1]["goalsFor"] += goals2;
    team2[1]["goalsAgainst"] += goals1;
    
    team1[1]["matchesPlayed"] += 1;
    team2[1]["matchesPlayed"] += 1;
    
    if(goals1 > goals2):
        team1[1]["wins"] += 1;
        team1[1]["points"] += 3;
        team2[1]["losses"] += 1;
    if(goals1 < goals2):
        team2[1]["wins"] += 1;
        team2[1]["points"] += 3;
        team1[1]["losses"] += 1;
    if(goals1 == goals2):
        team1[1]["points"] += 1;
        team2[1]["points"] += 1;


def main():
    with open('./teams.json', 'r') as data:
        teams = json.load(data);
    for team1 in teams.items():
        for team2 in teams.items():
            if(team1 != team2):
                play_match(team1, team2);
    standings = sorted(teams.items(), key=lambda k: (k[1].get('points'), float(k[1].get('goalsFor') / k[1].get('goalsAgainst'))), reverse=True);
    s = 1;
    for standing in standings:
        print(str(s) +'.' + standing[0] + ": " + str(standing[1]["points"]) + " " + 
                                       str(standing[1]["wins"]) + "W-" + str(standing[1]["matchesPlayed"] - 
                                        standing[1]["wins"] - standing[1]["losses"]) + 
                                       "D-" + str(standing[1]["losses"]) + "L-" + str(standing[1]["goalsFor"]) + "GF-" + 
                                       str(standing[1]["goalsAgainst"])+ "GA");
        s += 1;


main()