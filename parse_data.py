import os
import re
import csv
import json
import locale
import collections

baseDir = 'Predict_TV_Show_Cancelation'
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

def load_unparsed_json(whichJson):
    filename = whichJson + ".json"

    try:
        with open(os.path.join(baseDir, 'Data', filename), 'r') as f:
            return json.load(f)
    except:
        print("Could not load %s" %(filename))
        return None


