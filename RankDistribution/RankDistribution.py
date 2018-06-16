import json
import os

ProfileList = os.listdir("filteredprofiles")

SRDict = {}

for SR in range(1, 5001):
    SRDict["{}".format(SR)] = []

for Filename in ProfileList:
    File = open("filteredprofiles/{}".format(Filename), "r")
    Profile = json.load(File)
    File.close()

    SkillRating = Profile["competitive"]["general_stats"]["overall_stats"]["comprank"]
    print("Adding {} to {}".format(Filename, SkillRating))
    SRDict["{}".format(SkillRating)].append(Filename)

FullListFile = open("FullList.json", "w")
json.dump(SRDict, FullListFile)
FullListFile.close()

SRList = list(range(1, 5001))
TallyList = []
for SR in range(1, 5001):
    ListLength = len(SRDict["{}".format(SR)])
    print("{} list length is {}".format(SR, ListLength))
    TallyList.append(ListLength)

SmallListFile = open("SmallList.json", "w")
json.dump([SRList, TallyList], SmallListFile)
SmallListFile.close()