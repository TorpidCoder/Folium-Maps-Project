__author__ = "ResearchInMotion"

import folium
import json
import numpy as np
import vincent
import pandas as pd
from folium.plugins import MiniMap
from folium.plugins import MarkerCluster
from folium.plugins import Draw
from folium.plugins import HeatMap
from folium import plugins
from folium.plugins import MousePosition



import sys
import os
import subprocess

default_path = os.path.expanduser('/Users/sahilnagpal/')


def user_action(apath, cmd):
    ascript = '''
    -- apath - default path for dialogs to open too
    -- cmd   - "Select", "Save"
    on run argv
        set userCanceled to false
        if (count of argv) = 0 then
            tell application "System Events" to display dialog "argv is 0" ¬
                giving up after 10
        else
            set apath to POSIX file (item 1 of argv) as alias
            set action to (item 2 of argv) as text
        end if
        try
        if action contains "Select" then
            set fpath to POSIX path of (choose file default location apath ¬
                     without invisibles, multiple selections allowed and ¬
                     showing package contents)
            # return fpath as text
        else if action contains "Save" then
            set fpath to POSIX path of (choose file name default location apath)
        end if
        return fpath as text
        on error number -128
            set userCanceled to true
        end try
        if userCanceled then
            return "Cancel"
        else
            return fpath
        end if
    end run
    '''
    try:
        proc = subprocess.check_output(['osascript', '-e', ascript,
                                       apath, cmd])
        if 'Cancel' in proc.decode('utf-8'):  # User pressed Cancel button
            sys.exit('User Canceled')
        return proc.decode('utf-8')
    except subprocess.CalledProcessError as e:
            print('Python error: [%d]\n%s\n' % e.returncode, e.output)



# opens AppleScript choose file dialog and returns UNIX filename
fname = user_action(default_path, "Select").strip()

#generating the data points here
scatter_points = {
    'x': np.random.uniform(size=(100,)),
    'y': np.random.uniform(size=(100,)),
}

# Let's create the vincent chart.
scatter_chart = vincent.Scatter(scatter_points,
                                iter_idx='x',
                                width=600,
                                height=300)

# Let's convert it to JSON.
scatter_json = scatter_chart.to_json()

# Let's convert it to dict.
scatter_dict = json.loads(scatter_json)



print("The name of the file you have selected is : " ,  os.path.basename(fname))

delimeter = input("File Delimeter : ")

data = pd.read_csv(fname, sep=delimeter)


data = data.dropna()




latCol = input("Please enter the Latitude Column Name : ")
latRow = int(input("Index of Laitude Column in your file : "))

longCol = input("Please enter the Longitude Column Name : ")
lonRow = int(input("Index of Longitude Column in your file  : "))

#elevationRow = int(input("Index of Elevation Column in your file  : "))

# creating the map layer here
print("Creating the map here")
some_map = folium.Map(location=[data[latCol].mean(),data[longCol].mean()],zoom_start = 6)
minimap = MiniMap()   # creating the mini map here
draw = Draw()   # custom draw here



# cluster layer
mc = MarkerCluster()
mc.layer_name = 'Clusters'




for row in data.itertuples():
    popup = folium.Popup()
    folium.Vega(scatter_chart,height=350,width=650).add_to(popup)
    mc.add_child(folium.Marker(location=[row[latRow],row[lonRow]],
                            popup=popup))
    # mc.add_child(folium.Marker(location=[row[latRow], row[lonRow]],
    #                            popup=row[elevationRow]))

# heat map layer
stationArr = data[[latCol, longCol]].as_matrix()
heatmap = plugins.HeatMap(stationArr)

#putting the heat map layer name here
heatmap.layer_name = 'Heat Map'


# mouse position
MousePosition().add_to(some_map)


draw.add_to(some_map)
some_map.add_child(heatmap)
some_map.add_child(mc)
some_map.add_child(minimap)
folium.TileLayer("stamentoner").add_to(some_map)
folium.TileLayer("openstreetmap").add_to(some_map)
folium.LayerControl().add_to(some_map)
some_map.save('someMap.html')





