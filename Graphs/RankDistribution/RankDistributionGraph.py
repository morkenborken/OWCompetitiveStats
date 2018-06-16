from bokeh.io import output_file, save, show
from bokeh.plotting import figure
from bokeh.models import Title, LabelSet, ColumnDataSource, Legend
import json
from math import sqrt

#Loading and sorting data

SmallListFile = open("SmallList.json", "r")
SmallList = json.load(SmallListFile)
SmallListFile.close()

TotalNumUsers = sum(SmallList[1])
TotalSR = 0
SRBoundaries = [0, 1500, 2000, 2500, 3000, 3500, 4000, 4999]

#Figuring out percentage of users in each tier
UsersInGroup = [0]
PercentagePerGroup = [0] * 7
GroupIndex = 0
for i in range(len(SmallList[1])):
    TotalSR = TotalSR + (SmallList[1][i] * (i +1))
    if i < SRBoundaries[GroupIndex + 1]:
        UsersInGroup[GroupIndex] = UsersInGroup[GroupIndex] + SmallList[1][i]
    else:
        print("Users between {} and {}: {}".format(SRBoundaries[GroupIndex], SRBoundaries[GroupIndex + 1], UsersInGroup[GroupIndex]))
        GroupIndex = GroupIndex + 1
        UsersInGroup.append(0)
        UsersInGroup[GroupIndex] = UsersInGroup[GroupIndex] + SmallList[1][i]

MeanSR = TotalSR/TotalNumUsers
for i in range(len(PercentagePerGroup)):
    PercentagePerGroup[i] = 100 * round(UsersInGroup[i]/TotalNumUsers, 4)

print(PercentagePerGroup)
print("Mean SR = {}".format(MeanSR))
TotalVariance = 0.0
for i in range(len(SmallList[1])):
    TotalVariance = TotalVariance + (pow(i + 1 - MeanSR, 2) * SmallList[1][i])
Variance = TotalVariance/TotalNumUsers
Sigma = sqrt(Variance)
print("Variance = {}".format(Variance))
print("Sigma = {}".format(Sigma))
#Sort data to make the plot cleaner

PlotList = [[],[]]
for Count in range(198):
    PlotList[0].append(SmallList[0][(Count * 25 + 24)] + 12.5)
    PlotList[1].append(sum(SmallList[1][(Count * 25 + 24):(Count*25 + 49)]))

#Plotting

fill_color = ["#cd7f32", "#c0c0c0", "#d4af37", "#cccbca", "#9370db", "#f0ac48", "#ffe276"]

LabelsX = [1100, 1600, 2100, 2600, 3100, 3600, 4100]
LabelsY = [50, 50, 50, 50, 50, 300, 300]
#Replace with percentages
LabelsNames = list(map(str, PercentagePerGroup))
for i in range(len(LabelsNames)):
    LabelsNames[i] = LabelsNames[i].join(" %")

LabelsDict = dict(x=LabelsX, y=LabelsY, names=LabelsNames)
output_file("RankDistribution.html")
RankPlot = figure(plot_width=1600, plot_height=800, tools="pan,box_zoom,reset,save")


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
    DistributionGlyphs.append(RankPlot.vbar(x=GroupVBar[0], top=GroupVBar[1],
                fill_color=fill_color[GroupIndex], line_color=fill_color[GroupIndex], width=25))
    GroupIndex = GroupIndex + 1

RankPlot.title.text = "Overwatch Competitive Mode Rank Distribution"
RankPlot.title.align = "center"
RankPlot.title.text_color = "black"
RankPlot.title.text_font_size = "40px"
RankPlot.yaxis[0].axis_label = "Number of players"
RankPlot.xaxis[0].axis_label = "Skill Rating"

MeanGlyph = RankPlot.vbar(x=MeanSR, top=4500, fill_color="black", line_color="black", width=5)

LabelsSource = ColumnDataSource(LabelsDict)
LabelsLayout = LabelSet(x="x", y="y", text="names", source=LabelsSource, level="glyph",
    text_color="black", render_mode="css", border_line_color="black", border_line_alpha=1.0,
    background_fill_alpha=0.5, background_fill_color="white")

RankPlot.add_layout(LabelsLayout)

DistributionLegend = Legend(items=[
                        ("Mean SR", [MeanGlyph]),
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

RankPlot.add_layout(DistributionLegend)
show(RankPlot)