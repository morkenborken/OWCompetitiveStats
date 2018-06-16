import os
import json
import shutil

FileList = os.listdir("profiles")
FilteredFileList = os.listdir("filteredprofiles")
for Filename in FileList:
    if Filename not in FilteredFileList:
        print("Opening {}".format(Filename))
        UserFile = open("profiles/{}".format(Filename), "r")
        profile = json.load(UserFile)
        UserFile.close()
        
        BrigQPPlaytime = BrigCompPlaytime = 0
        
        if (profile["quickplay"]["hero_playtime"] != None) and ("brigitte" in profile["quickplay"]["hero_playtime"]):
            BrigQPPlaytime = profile["quickplay"]["hero_playtime"]["brigitte"]
        if "brigitte" in profile["competitive"]["hero_playtime"]:
            BrigCompPlaytime = profile["competitive"]["hero_playtime"]["brigitte"]
            
        print("{} : QP: {}, Comp: {}".format(Filename, BrigQPPlaytime, BrigCompPlaytime))
        if (BrigQPPlaytime != 0) or (BrigCompPlaytime != 0):
            shutil.copyfile("profiles/{}".format(Filename), "filteredprofiles/{}".format(Filename))
            print("Copied {}".format(Filename))

