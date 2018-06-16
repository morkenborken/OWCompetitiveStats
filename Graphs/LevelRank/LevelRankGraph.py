from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.models import Title, LabelSet, ColumnDataSource, Legend
import json 

FullListFile = open("FullList.json", "r")
FullList = json.load(FullListFile)
FullListFile.close()

#Sort into lists
LevelSumList = [[],[]]
SRBoundaries = [0, 1500, 2000, 2500, 3000, 3500, 4000, 4999]
TierIndex = 0
TierLevelSumList = [0]
UsersInTier = [0]
TierAvgLevelList = [] 

for SR in range(1, 5001):
    NumUsers = LevelSum = 0
    for User in FullList["{}".format(SR)]:
        NumUsers = NumUsers + 1
        LevelSum = LevelSum + User[1]
    
    LevelSumList[0].append(LevelSum)
    LevelSumList[1].append(NumUsers)

    if (SR-1) < SRBoundaries[TierIndex + 1]:
        UsersInTier[TierIndex] = UsersInTier[TierIndex] + NumUsers
        TierLevelSumList[TierIndex] = TierLevelSumList[TierIndex] + LevelSum
    else:
        TierAvgLevelList.append(int(round(TierLevelSumList[TierIndex]/UsersInTier[TierIndex], 0)))
        print("{} - {} \nAverage Level: {} \n Users: {}".format(SRBoundaries[TierIndex], 
                SRBoundaries[TierIndex + 1], TierAvgLevelList[TierIndex], UsersInTier[TierIndex]))
        TierIndex = TierIndex + 1
        UsersInTier.append(NumUsers)
        TierLevelSumList.append(LevelSum)

#Sort data for better plots
PlotList = [[],[]]
for Count in range(198):
    PlotList[0].append(Count * 25 + 37.5)
    LevelSum = UsersInRange = 0

    for i in range(25):
        LevelSum = LevelSum + LevelSumList[0][(Count * 25) + 24 + i]
        UsersInRange = UsersInRange + LevelSumList[1][(Count * 25) + 24 + i]
    if UsersInRange > 0:
        PlotList[1].append(LevelSum/UsersInRange)
    else:
        PlotList[1].append(0)

#Plotting

fill_color = ["#cd7f32", "#c0c0c0", "#d4af37", "#cccbca", "#9370db", "#f0ac48", "#ffe276"]

LabelsX = [1100, 1600, 2100, 2600, 3100, 3600, 4100]
LabelsY = [25, 25, 25, 25, 25, 25, 25]

#Replace with percentages
LabelsNames = list(map(str, TierAvgLevelList))

LabelsDict = dict(x=LabelsX, y=LabelsY, names=LabelsNames)

output_file("LevelRank.html")
LevelPlot = figure(plot_width=1600, plot_height=800, tools="pan,box_zoom,reset,save")

#Sort into separate datasets for separate glyphs
GroupVBars = []
GroupIndex = 0
for i in range(len(PlotList[0])):
    if PlotList[0][i] < SRBoundaries[GroupIndex]:
        GroupVBars[GroupIndex - 1][0].append(PlotList[0][i])
        GroupVBars[GroupIndex - 1][1].append(PlotList[1][i])
    else:
        GroupIndex = GroupIndex + 1
        GroupVBars.append([[],[]])
        GroupVBars[GroupIndex - 1][0].append(PlotList[0][i])
        GroupVBars[GroupIndex - 1][1].append(PlotList[1][i])

DistributionGlyphs = []
GroupIndex = 0
for GroupVBar in GroupVBars:
    DistributionGlyphs.append(LevelPlot.vbar(x=GroupVBar[0], top=GroupVBar[1],
                fill_color=fill_color[GroupIndex], line_color=fill_color[GroupIndex], width=25))
    GroupIndex = GroupIndex + 1

LevelPlot.title.text = "Overwatch Competitive Mode Average Level at a Skill Rating"
LevelPlot.title.align = "center"
LevelPlot.title.text_color = "black"
LevelPlot.title.text_font_size = "40px"
LevelPlot.yaxis[0].axis_label = "Average Level"
LevelPlot.xaxis[0].axis_label = "Skill Rating"

LabelsSource = ColumnDataSource(LabelsDict)
LabelsLayout = LabelSet(x="x", y="y", text="names", source=LabelsSource, level="glyph",
    text_color="black", render_mode="css", border_line_color="black", border_line_alpha=1.0,
    background_fill_alpha=0.5, background_fill_color="white")

LevelPlot.add_layout(LabelsLayout)

DistributionLegend = Legend(items=[
                        ("Bronze", [DistributionGlyphs[0]]),
                        ("Silver", [DistributionGlyphs[1]]),
                        ("Gold", [DistributionGlyphs[2]]),
                        ("Platinum", [DistributionGlyphs[3]]),
                        ("Diamond", [DistributionGlyphs[4]]),
                        ("Master", [DistributionGlyphs[5]]),
                        ("Grandmaster", [DistributionGlyphs[6]])
                        ], background_fill_color="#0055ff",
                        background_fill_alpha=0.25,
                        border_line_color="black")

LevelPlot.add_layout(DistributionLegend)
show(LevelPlot)
