from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.models import Title, LabelSet, ColumnDataSource, Legend
import json 

FullListFile = open("FullList.json", "r")
FullList = json.load(FullListFile)
FullListFile.close()

#Sort into lists
WRSumList = [[],[]]
SRBoundaries = [0, 1500, 2000, 2500, 3000, 3500, 4000, 4999]
TierIndex = 0
TierWRSumList = [0]
UsersInTier = [0]
TierAvgWRList = []

for SR in range(1, 5001):
    NumUsers = WRSum = 0
    for User in FullList["{}".format(SR)]:
        NumUsers = NumUsers + 1
        WRSum = WRSum + User[1]
    
    WRSumList[0].append(WRSum)
    WRSumList[1].append(NumUsers)

    if (SR-1) < SRBoundaries[TierIndex + 1]:
        UsersInTier[TierIndex] = UsersInTier[TierIndex] + NumUsers
        TierWRSumList[TierIndex] = TierWRSumList[TierIndex] + WRSum
    else:
        TierAvgWRList.append(round(TierWRSumList[TierIndex]/UsersInTier[TierIndex], 2))
        print("{} - {} \nAverage Winrate: {} \n Users: {}".format(SRBoundaries[TierIndex], 
                SRBoundaries[TierIndex + 1], TierAvgWRList[TierIndex], UsersInTier[TierIndex]))
        TierIndex = TierIndex + 1
        UsersInTier.append(NumUsers)
        TierWRSumList.append(WRSum)

#Sort data for better plots
PlotList = [[],[]]
for Count in range(198):
    PlotList[0].append(Count * 25 + 37.5)
    WRSum = UsersInRange = 0

    for i in range(25):
        WRSum = WRSum + WRSumList[0][(Count * 25) + 24 + i]
        UsersInRange = UsersInRange + WRSumList[1][(Count * 25) + 24 + i]
    if UsersInRange > 0:
        PlotList[1].append(WRSum/UsersInRange)
    else:
        PlotList[1].append(0)

#Plotting

fill_color = ["#cd7f32", "#c0c0c0", "#d4af37", "#cccbca", "#9370db", "#f0ac48", "#ffe276"]

LabelsX = [1100, 1600, 2100, 2600, 3100, 3600, 4100]
LabelsY = [25, 25, 25, 25, 25, 25, 25]

#Replace with percentages
LabelsNames = list(map(str, TierAvgWRList))
for i in range(len(LabelsNames)):
    LabelsNames[i] = LabelsNames[i].join(" %")

LabelsDict = dict(x=LabelsX, y=LabelsY, names=LabelsNames)

output_file("WRvsSR.html")
WRPlot = figure(plot_width=1600, plot_height=800, tools="pan,box_zoom,reset,save")

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
    DistributionGlyphs.append(WRPlot.vbar(x=GroupVBar[0], top=GroupVBar[1],
                fill_color=fill_color[GroupIndex], line_color=fill_color[GroupIndex], width=25))
    GroupIndex = GroupIndex + 1

WRPlot.title.text = "Overwatch Competitive Mode Winrate vs Skill Rating"
WRPlot.title.align = "center"
WRPlot.title.text_color = "black"
WRPlot.title.text_font_size = "40px"
WRPlot.yaxis[0].axis_label = "Average Winrate"
WRPlot.xaxis[0].axis_label = "Skill Rating"

LabelsSource = ColumnDataSource(LabelsDict)
LabelsLayout = LabelSet(x="x", y="y", text="names", source=LabelsSource, level="glyph",
    text_color="black", render_mode="css", border_line_color="black", border_line_alpha=1.0,
    background_fill_alpha=0.5, background_fill_color="white")

WRPlot.add_layout(LabelsLayout)

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

WRPlot.add_layout(DistributionLegend)
show(WRPlot)