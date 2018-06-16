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
    Prestige = Profile["competitive"]["general_stats"]["overall_stats"]["prestige"]
    Level = Profile["competitive"]["general_stats"]["overall_stats"]["level"]
    TrueLevel = (Prestige * 100) + Level
    print("Adding {} to {}".format(Filename, SkillRating))
    SRDict["{}".format(SkillRating)].append([Filename, TrueLevel])

FullListFile = open("FullList.json", "w")
json.dump(SRDict, FullListFile)
FullListFile.close()
