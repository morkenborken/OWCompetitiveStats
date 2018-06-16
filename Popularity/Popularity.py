import json
import os
import sys

ProfileList = os.listdir("filteredprofiles")

FullList = [[] for i in range(5000)]
TotalSize = 0
for Filename in ProfileList:
    print("Opening {}".format(Filename))
    File = open("filteredprofiles/{}".format(Filename), "r")
    Profile = json.load(File)
    File.close()

    SkillRating = int(Profile["competitive"]["general_stats"]["overall_stats"]["comprank"])
    HeroList = Profile["competitive"]["hero_playtime"]

    print("Adding {} to index {}".format(Filename, SkillRating - 1))
    FullList[SkillRating-1].append(HeroList)


FullListFile = open("FullList.json", "w")
json.dump(FullList, FullListFile)
FullListFile.close()
