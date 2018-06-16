from bokeh.io import output_file, save, show
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter
import json
from copy import deepcopy
FullListFile = open("FullList.json", "r")
FullList = json.load(FullListFile)
FullListFile.close()

HeroKeyDict = {
    "doomfist": "Doomfist",
    "genji": "Genji",
    "mccree": "McCree",
    "pharah": "Pharah",
    "reaper": "Reaper",
    "soldier76": "Soldier: 76",
    "sombra": "Sombra",
    "tracer": "Tracer",
    "bastion": "Bastion",
    "hanzo": "Hanzo",
    "junkrat": "Junkrat",
    "mei": "Mei",
    "torbjorn": "Torbjörn",
    "widowmaker": "Widowmaker",
    "dva": "D.Va",
    "orisa": "Orisa",
    "reinhardt": "Reinhardt",
    "roadhog": "Roadhog",
    "winston": "Winston",
    "zarya": "Zarya",
    "ana": "Ana",
    "brigitte": "Brigitte",
    "lucio": "Lúcio",
    "mercy": "Mercy",
    "moira": "Moira",
    "symmetra": "Symmetra",
    "zenyatta": "Zenyatta"
}

RoleHeroDict = {
    "Offense": ["doomfist", "genji", "mccree", "pharah", "reaper", "soldier76", "sombra", "tracer"],
    "Defense": ["bastion", "junkrat","mei", "torbjorn", "widowmaker"],
    "Tank": ["dva", "orisa", "reinhardt", "roadhog", "winston", "zarya"],
    "Support": ["ana", "lucio", "mercy", "moira", "symmetra", "zenyatta"]
}

RoleTimeDict = {
    "Offense": 0,
    "Defense": 0,
    "Tank": 0,
    "Support": 0
}

HeroTimeDict = {
    "Doomfist": 0,
    "Genji": 0,
    "McCree": 0,
    "Pharah": 0,
    "Reaper": 0,
    "Soldier: 76": 0,
    "Sombra": 0,
    "Tracer": 0,
    "Bastion": 0,
    "Hanzo": 0,
    "Junkrat": 0,
    "Mei": 0,
    "Torbjörn": 0,
    "Widowmaker": 0,
    "D.Va": 0,
    "Orisa": 0,
    "Reinhardt": 0,
    "Roadhog": 0,
    "Winston": 0,
    "Zarya": 0,
    "Ana": 0,
    "Brigitte": 0,
    "Lúcio": 0,
    "Mercy": 0,
    "Moira": 0,
    "Symmetra": 0,
    "Zenyatta": 0
}

SRBoundaries = [0, 1500, 2000, 2500, 3000, 3500, 4000, 4999]
Tiers = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]

#Sort into lists
TotalHeroTime = deepcopy(HeroTimeDict)
TierHeroTime = [deepcopy(HeroTimeDict) for i in range(len(SRBoundaries) - 1)]
TotalRoleTime = deepcopy(RoleTimeDict)
TierRoleTime = [deepcopy(RoleTimeDict) for i in range(len(SRBoundaries) - 1)]
TierIndex = 0

for i in range(5000):
    for HeroList in FullList[i]:
        for HeroKey in HeroList.keys():
            TotalHeroTime[HeroKeyDict[HeroKey]] = TotalHeroTime[HeroKeyDict[HeroKey]] + HeroList[HeroKey]
        for RoleKey in RoleHeroDict.keys():
            for HeroKey in RoleHeroDict[RoleKey]:
                if HeroKey in HeroList:
                    TotalRoleTime[RoleKey] = TotalRoleTime[RoleKey] + HeroList[HeroKey]

        if i < SRBoundaries[TierIndex + 1]:
            for HeroKey in HeroList.keys():
                TierHeroTime[TierIndex][HeroKeyDict[HeroKey]] = \
                TierHeroTime[TierIndex][HeroKeyDict[HeroKey]] + HeroList[HeroKey]
            for RoleKey in RoleHeroDict.keys():
                for HeroKey in RoleHeroDict[RoleKey]:
                    if HeroKey in HeroList:
                        TierRoleTime[TierIndex][RoleKey] = \
                        TierRoleTime[TierIndex][RoleKey] + HeroList[HeroKey]
        else:
            TierIndex = TierIndex + 1
            print("Finished Tier {}".format(TierIndex))
            for HeroKey in HeroList.keys():
                TierHeroTime[TierIndex][HeroKeyDict[HeroKey]] = \
                TierHeroTime[TierIndex][HeroKeyDict[HeroKey]] + HeroList[HeroKey]
            for RoleKey in RoleHeroDict.keys():
                for HeroKey in RoleHeroDict[RoleKey]:
                    if HeroKey in HeroList:
                        TierRoleTime[TierIndex][RoleKey] = TierRoleTime[TierIndex][RoleKey] + HeroList[HeroKey]

#Sorting the lists a bit more
UnsortedRoleList = list(TotalRoleTime.keys())
UnsortedRoleList.append("DPS")
Top = list(TotalRoleTime.values())
UnsortedColorList = ["#f8911b", "#9adaf4", "#a9958e", "#fee16c", "#8c3a3a"]
UnsortedURLList = ["Offense.png", "Defense.png", "Tank.png", "Support.png", "DPS.png"]
TotalTime = sum(Top)
Top.append(Top[0] + Top[1])
Indices, Top = zip(*[i for i in sorted(enumerate(Top), key=lambda x:x[1], reverse=True)])
x_range = [UnsortedRoleList[i] for i in Indices]
URLList = [UnsortedURLList[i] for i in Indices]
ColorList = [UnsortedColorList[i] for i in Indices]
TopNormalized = list(map(lambda x: x/TotalTime, Top))

#Plotting
output_file("RolesPopularity.html")
PopularityPlot = figure(x_range=x_range, plot_width=1600, plot_height=800, 
                        tools="pan,box_zoom,reset,save")
PopularityPlot.vbar(x=x_range, top=TopNormalized, width=0.9, 
            fill_color=ColorList, line_color="black")
PopularityPlot.image_url(x=x_range, url=URLList, y=list(map(lambda x: x*0.5, TopNormalized)),
                         w=0.35, h=0.07, anchor="center")

PopularityPlot.title.text = "Overwatch Competitive Mode Role Playtime"
PopularityPlot.title.align = "center"
PopularityPlot.title.text_color = "black"
PopularityPlot.title.text_font_size = "40px"
PopularityPlot.yaxis[0].axis_label = "Playtime as Percentage of Total"
PopularityPlot.xaxis[0].axis_label = "Role"
PopularityPlot.yaxis[0].axis_label_text_font_size = "20px"
PopularityPlot.xaxis[0].axis_label_text_font_size = "20px"
PopularityPlot.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")

#Repeating for each tier

XRangeList, IndicesList, TopList, URLsList, NormalizedTopList, Plots, ColorsList = ([] for i in range(7))
GraphIndex = 0
for RoleTime in TierRoleTime:
    print(GraphIndex)
    XRangeList.append([])
    IndicesList.append([])
    TopList.append([])
    URLsList.append([])
    ColorsList.append([])
    TopList[GraphIndex] = list(RoleTime.values())
    TierTotalTime = sum(TopList[GraphIndex])
    TopList[GraphIndex].append(TopList[GraphIndex][0] + TopList[GraphIndex][1])
    IndicesList[GraphIndex], TopList[GraphIndex] = zip(*[i for i in \
                                                        sorted(enumerate(TopList[GraphIndex]),
                                                        key=lambda x:x[1], reverse=True)])
    print("{} {}".format(len(IndicesList[GraphIndex]), len(UnsortedRoleList)))
    XRangeList[GraphIndex] = [UnsortedRoleList[i] for i in IndicesList[GraphIndex]]
    URLsList[GraphIndex] = [UnsortedURLList[i] for i in IndicesList[GraphIndex]]
    ColorsList[GraphIndex] = [UnsortedColorList[i] for i in IndicesList[GraphIndex]]

    NormalizedTopList.append(list(map(lambda x: x/TierTotalTime, TopList[GraphIndex])))

    Plots.append(figure(x_range=XRangeList[GraphIndex], plot_width=1600, plot_height=800, 
                        tools="pan,box_zoom,reset,save"))
    Plots[GraphIndex].vbar(x=XRangeList[GraphIndex], top=NormalizedTopList[GraphIndex],
                    width=0.9, fill_color=ColorsList[GraphIndex], line_color="black")

    Plots[GraphIndex].image_url(x=XRangeList[GraphIndex], url=URLsList[GraphIndex],
            y=list(map(lambda x: x*0.5, NormalizedTopList[GraphIndex])),
             w=0.35, h=0.07, anchor="center")

    Plots[GraphIndex].title.text = "Overwatch Competitive Mode Role Playtime in {}".format(Tiers[GraphIndex])
    Plots[GraphIndex].title.align = "center"
    Plots[GraphIndex].title.text_color = "black"
    Plots[GraphIndex].title.text_font_size = "40px"
    Plots[GraphIndex].yaxis[0].axis_label = "Playtime as Percentage of Total"
    Plots[GraphIndex].xaxis[0].axis_label = "Role"
    Plots[GraphIndex].yaxis[0].axis_label_text_font_size = "20px"
    Plots[GraphIndex].xaxis[0].axis_label_text_font_size = "20px"
    Plots[GraphIndex].yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    GraphIndex = GraphIndex + 1

FullPlotList = [PopularityPlot]
FullPlotList.extend(Plots)
show(column(FullPlotList))
