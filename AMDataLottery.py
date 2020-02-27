# -*- coding: utf-8 -*-

#Import packages
import numpy as np
import pandas as pd
import imageio
import matplotlib.pyplot as plt

#Set Random Seed
np.random.seed(12345)


#List of contestants in order of purchase
Contestants = ["Mary Q",
				"Will N",
				"Will C",
				"David D",
				"Sarah H",
				"Rachel P",
				"Margaret C",
				"Eric M",
				"Francisco R",
				"Meghana G",
				"Shivram V",
				"Shazaib S"]
NumContestants = len(Contestants)


#List of Columns for df
colNames = ["Previous Total",
            "Total",
            "Win this round?",
            "Winner",
            "Winning Value",
            "Won on Step #",
            "W",
            "AW",
            "L"]

df = pd.DataFrame(np.zeros(shape=(len(Contestants), len(colNames))),
                  columns = colNames, index = Contestants)



#Looping through to find winners
winners = []
n = 0
while len(winners) < 2:
    #Start for next step
    n = n+1
    
    #Random Draw
    df["Previous Total"] = df["Total"]
    df["Added on Step #%d" % n] = 4 * np.random.rand(NumContestants)
    df["Total"] = df["Previous Total"] + df["Added on Step #%d" % n]
    
    #Determine if there are any winners
    df["Win this round?"] = (df["Total"] >= 100)
    for x in Contestants:
        if df.loc[x, "Win this round?"] == True and df.loc[x, "Winner"] == False:
            winners.append(x)
            df.loc[x, "Winning Value"] = df.loc[x, "Total"]
            df.loc[x, "Won on Step #"] = n
            df.loc[x, "Winner"] = True
    
        #Set winning value and make other values zero
        if df.loc[x, "Winner"] == True:
            df.loc[x, "Previous Total"] = 0
            df.loc[x, "Added on Step #%d" % n] = 0
        
    #Create Plots for Step n
    N = len(Contestants)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.75       # the width of the bars: can also be len(x) sequence
    
    p1 = plt.bar(ind, df["Previous Total"], width, color='darkred')
    p2 = plt.bar(ind, df["Added on Step #%d" % n], width, color='lightcoral',
                 bottom=df["Previous Total"])
    p3 = plt.bar(ind, df["Winning Value"], width, color='goldenrod',
                 bottom=df["Previous Total"])
    
    plt.title('AMData Lottery: Step #%d' % n)
    plt.xticks(ind, Contestants, rotation='vertical')
    plt.yticks(np.arange(0, 120 + 0.01, 25))
    plt.axhline(y=100, linestyle='--')
    
    plt.savefig('ExportedGraphs/%d.png' % n, bbox_inches="tight")


#Sort and find the winners
df_sorted = df.sort_values(by=["Winner", "Won on Step #", "Winning Value"], 
                            ascending=[False, True, False])    
winner1 = df_sorted.index[0]
winner2 = df_sorted.index[1]
winners = [winner1, winner2]


#Create Final Graph
for x in Contestants:
    if df.loc[x, "Winner"] == True:
        df.loc[x, "AW"] = df.loc[x, "Total"]
    if df.loc[x, "Winner"] == False:
        df.loc[x, "L"] = df.loc[x, "Total"]
        
df.loc[winner1, "W"] = df.loc[winner1, "Winning Value"]
df.loc[winner1, "AW"] = 0

df.loc[winner2, "W"] = df.loc[winner2, "Winning Value"] 
df.loc[winner2, "AW"] = 0 

N = len(Contestants)
ind = np.arange(N)    # the x locations for the groups
width = 0.75       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df["W"], width, color='darkgoldenrod')
p2 = plt.bar(ind, df["AW"], width, color='saddlebrown')
p3 = plt.bar(ind, df["L"], width, color='black')

plt.title('The winners are %s and %s' % (winner1, winner2))
plt.xticks(ind, Contestants, rotation='vertical')
plt.yticks(np.arange(0, 120 + 0.01, 25))
plt.axhline(y=100, linestyle='--')

plt.savefig('ExportedGraphs/%d.png' % (n+1), bbox_inches="tight")



                        
#Create GIF
gif_path = "AMDataLottery.gif"
frames_path = "ExportedGraphs/{i}.png"

with imageio.get_writer(gif_path, mode='I', duration = 0.5) as writer:
    for i in range(1, n + 2):
        writer.append_data(imageio.imread(frames_path.format(i=i)))

                 