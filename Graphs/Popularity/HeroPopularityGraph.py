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
UnsortedHeroList = list(TotalHeroTime.keys())
Top = list(TotalHeroTime.values())
UnsortedColorList = ["#df4e34", "#84fe01", "#8d3a3a", "#1b65c5", "#272725", "#5870b6", "#761c9c", "#f8911b",
                "#6e994d", "#938848", "#d39309", "#9adaf4", "#ff6200", "#6f6fad",
                "#ff80d0", "#db9a00", "#a9958e", "#b58c72", "#4d505c", "#f471a8",
                "#ccc2ad", "#73342b", "#8bec22", "#fee16c", "#691cce", "#5cecff", "#c69b00"]
Indices, Top = zip(*[i for i in sorted(enumerate(Top), key=lambda x:x[1], reverse=True)])
TotalTime = sum(Top)
x_range = [UnsortedHeroList[i] for i in Indices]
ColorList = [UnsortedColorList[i] for i in Indices]
TopNormalized = list(map(lambda x: x/TotalTime, Top))

#Plotting
output_file("HeroesPopularity.html")
PopularityPlot = figure(x_range=x_range, plot_width=1600, plot_height=800, 
                        tools="pan,box_zoom,reset,save")
PopularityPlot.vbar(x=x_range, top=TopNormalized, width=1, 
            fill_color=ColorList, line_color="black")

PopularityPlot.title.text = "Overwatch Competitive Mode Hero Playtime"
PopularityPlot.title.align = "center"
PopularityPlot.title.text_color = "black"
PopularityPlot.title.text_font_size = "40px"
PopularityPlot.yaxis[0].axis_label = "Playtime as Percentage of Total"
PopularityPlot.xaxis[0].axis_label = "Hero"
PopularityPlot.yaxis[0].axis_label_text_font_size = "20px"
PopularityPlot.xaxis[0].axis_label_text_font_size = "20px"
PopularityPlot.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")

#Repeating for each tier
XRangeList, IndicesList, TopList, ColorsList, NormalizedTopList, Plots = ([] for i in range(6))
GraphIndex = 0
for HeroTime in TierHeroTime:
    print(GraphIndex)
    XRangeList.append([])
    IndicesList.append([])
    TopList.append([])
    ColorsList.append([])
    IndicesList[GraphIndex], TopList[GraphIndex] = zip(*[i for i in \
                                                        sorted(enumerate(list(HeroTime.values())),
                                                        key=lambda x:x[1], reverse=True)])
    TopList[GraphIndex] = list(TopList[GraphIndex])
    TierTotalTime = sum(TopList[GraphIndex])
    XRangeList[GraphIndex] = [UnsortedHeroList[i] for i in IndicesList[GraphIndex]]
    ColorsList[GraphIndex] = [UnsortedColorList[i] for i in IndicesList[GraphIndex]]
    NormalizedTopList.append(list(map(lambda x: x/TierTotalTime, TopList[GraphIndex])))

    Plots.append(figure(x_range=XRangeList[GraphIndex], plot_width=1600, plot_height=800, 
                        tools="pan,box_zoom,reset,save"))

    Plots[GraphIndex].vbar(x=XRangeList[GraphIndex], top=NormalizedTopList[GraphIndex], width=1, 
            fill_color=ColorsList[GraphIndex], line_color="black")

    Plots[GraphIndex].title.text = "Overwatch Competitive Mode Hero Playtime in {}".format(Tiers[GraphIndex])
    Plots[GraphIndex].title.align = "center"
    Plots[GraphIndex].title.text_color = "black"
    Plots[GraphIndex].title.text_font_size = "40px"
    Plots[GraphIndex].yaxis[0].axis_label = "Playtime as Percentage of Total"
    Plots[GraphIndex].xaxis[0].axis_label = "Hero"
    Plots[GraphIndex].yaxis[0].axis_label_text_font_size = "20px"
    Plots[GraphIndex].xaxis[0].axis_label_text_font_size = "20px"
    Plots[GraphIndex].yaxis[0].formatter = NumeralTickFormatter(format="0.00%")
    GraphIndex = GraphIndex + 1

FullPlotList = [PopularityPlot]
FullPlotList.extend(Plots)
show(column(FullPlotList))
