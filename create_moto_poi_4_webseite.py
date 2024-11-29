# ##########################################################################################
# Hans Straßgütl
#       Pulls data from Openstreetmaps using the OverpassTurbo API.
#       Build Point of Interest in 2 KML formats: OruxMaps and OrganicMaps
#       
#       Uses a commandline paramater AND a JSON file. See readme-licence for details
#           
# ------------------------------------------------------------------------------------------
# Version:
#	2024 02 		Initial start of coding
#	2024 11 		Now includes: GPX, GPI, KML, KML for Organic Maps
#
# ##########################################################################################

import sys
import argparse
import ast  # Module for safely evaluating strings containing Python expressions
import requests
import shutil
import simplekml
import os
import subprocess
import xml.etree.ElementTree as ET

# ...................................................
# Where do I find my utils to be imported? Set your path here!
sys.path.append("C:\\SynologyDrive\\Python\\00_import_h_utils")
try:
    import h_utils                              # type: ignore
except Exception as e:
    print(f"Error importing utils: {e}")



# ------------------------------------------------------------------------------------------
#   ____      _       ___                                     
#  / ___| ___| |_    / _ \__   _____ _ __ _ __   __ _ ___ ___ 
# | |  _ / _ \ __|  | | | \ \ / / _ \ '__| '_ \ / _` / __/ __|
# | |_| |  __/ |_   | |_| |\ V /  __/ |  | |_) | (_| \__ \__ \
#  \____|\___|\__|___\___/  \_/ \___|_|  | .__/ \__,_|___/___/
#               |_____|                  |_|                  
# ------------------------------------------------------------------------------------------
'''
    Send Query to Overpass and download data
    Return JSON
'''
def download_data(query):
    overpass_url = "http://overpass-api.de/api/interpreter"
    # print(query)
    response = requests.get(overpass_url, params={"data": query})
    if response.status_code == 200:
        results = response.json()  # Parse the JSON response
        # print(results)
    else:
        print(f"Error: {response.status_code}")
        # print(response.text)
    return results # parsed data into JSON

# ------------------------------------------------------------------------------------------
#  _  ____  __ _         ___                        _      
# | |/ /  \/  | |       / _ \ _ __ __ _  __ _ _ __ (_) ___ 
# | ' /| |\/| | |      | | | | '__/ _` |/ _` | '_ \| |/ __|
# | . \| |  | | |___   | |_| | | | (_| | (_| | | | | | (__ 
# |_|\_\_|  |_|_____|___\___/|_|  \__, |\__,_|_| |_|_|\___|
#                  |_____|        |___/                    
# ------------------------------------------------------------------------------------------
def rework_kml_for_organic(kml_path, icon_color):
    kml_file_name, kml_tmp_file_name = h_utils.make_short_name(kml_path, 'kml')
    kml_tmp = open(kml_tmp_file_name, "w", encoding='utf-8')                # Open a Tempfile. Will be deleted later

    with open(kml_file_name, "r", encoding='utf-8') as kml_file:
        data = kml_file.readlines()                                         # read data line by line   
    
    # rework kml file as Textfile. remove all leading blanks and attach a new line command.
    for x in data:
        x = x.strip()
        x = x + '\n'
        kml_tmp.writelines(x)
    kml_tmp.close()
    kml_file.close()

    # Get the reworked file
    with open(kml_tmp_file_name, "r", encoding='utf-8') as kml_file:
        data = kml_file.readlines()                                         # read data line by line 
    kml_file.close()

    # Now delete the initial KML file and write out the new one into it
    kml_final = open(kml_file_name, "w", encoding='utf-8')
    is_placemark = False
    for x in data:
        kml_final.writelines(x)
        if x.find('<Placemark')  != -1 : is_placemark = True
        if x.find('</Placemark') != -1 : is_placemark = False
        if is_placemark :
            if x.find('<name>') != -1 :
                kml_final.writelines('<Snippet maxLines="0"/>\n')
                kml_final.writelines('<styleUrl>#' + icon_color + '</styleUrl>\n')
    kml_final.close()
    os.remove(kml_tmp_file_name)        

def make_names(clear_name):
    # Some basic definitions
    kml_name            = clear_name+"-global.kml"                            # type: ignore
    kml_oroux           = clear_name+"-orux-global.kml"                          # type: ignore
    kml_organic         = clear_name+"-organic-global.kml"                          # type: ignore
    gpx_name            = clear_name+"-global.gpx"                            # type: ignore
    gpi_name            = clear_name+"-global.gpi"                            # type: ignore                                         
    return(kml_name,kml_oroux, kml_organic,gpx_name,gpi_name)

def make_waypoints(data):
    coords = []
    for element in data['elements']:
        if element['type'] == 'node':
            lon = element['lon']
            lat = element['lat']
        elif 'center' in element:
            lon = element['center']['lon']
            lat = element['center']['lat']
        if 'tags' in element:
            if 'opening_hours' in element['tags']:
                descript = 'Opening Hours: ' + (element['tags']['opening_hours'])
            else:
                descript = ''
            if 'name' in element['tags']:
                name = (element['tags']['name'])
            else:
                name = "NoName"
        else:
            name = "NoName"
        if name != "NoName":
            new_waypoint = {"name": name, "description": descript, "lat": lat, "lon": lon}
            # print(new_waypoint)
            coords.append(new_waypoint)
    return(coords)


def make_gpx_gpi(brand_or_name, garmin_icon, organic_color):
    # Use an f-string to insert the variable into the query
    if brand_or_name == "GENERIC":
        overpass_query = f"""
[out:json][timeout:2400];
(
nwr["shop"="motorcycle"]["brand"!~".*"];
);
out center;
"""
    else:
        overpass_query = f"""
[out:json][timeout:2400];
(
nwr["shop"="motorcycle"]["brand"~".*{brand_or_name}.*",i];
nwr["shop"="motorcycle"]["name"~".*{brand_or_name}.*",i];
);
out center;
"""
                             
    print("Working on:      " + brand_or_name)
    # .......................................................................
    # Perform the Overpass query
    # .......................................................................
    data = download_data(overpass_query)
    # .......................................................................
    # convert to GeoDataFrame
    # .......................................................................
    # Collect coords into list
    coords = make_waypoints(data)
    # Some basic definitions
    kml_name, kml_orux_name, kml_organic_name, gpx_name, gpi_name = make_names(brand_or_name)
    my_path_to_icon = "http://motorradtouren.de/pins/bmp_4_oruxmaps/"
    orux_icon = my_path_to_icon + brand_or_name+".bmp"
    # Convert GeoDataFrame to GPX
    h_utils.create_gpx_with_symbols(coords, gpx_name, garmin_icon )

    # Get the absolute path to the bitmap
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of run.py
    bitmap_path = os.path.join(script_dir, "BMP", brand_or_name+".bmp")

    # Construct the GPSBabel command
    gpsbabel_command = [
        r"C:\Program Files\GPSBabel\GPSBabel.exe",
        "-w",
        "-i", "gpx",
        "-f", gpx_name ,
        "-o", f"garmin_gpi,bitmap={bitmap_path},unique=1",
        "-F", gpi_name
    ]
    # Run the command
    rc = subprocess.run(gpsbabel_command)


    # ----------------------------------------------------------------            
    # All KML here
    # Convert GeoDataFrame to KML using simplekml
    # ----------------------------------------------------------------            
    # In a first run, create a standard KML with no icons
    kml = simplekml.Kml(name="<![CDATA["+brand_or_name+"]]>", visibility = "1" , open ="1", atomauthor = "Hans Straßgütl" , atomlink = "https://gravelmaps.de"  )  
    for element in coords:
        pt2 = kml.newpoint(name='<![CDATA[' + element["name"] + ']]>',coords=[(element["lon"], element["lat"])], description = element["description"] )
    kml.save(kml_name)                                                      # Now the standard KML is saved.
    shutil.copy2(kml_name, kml_organic_name)                                # Making sure that the standard KML isn't touched while reworking for Organic Maps

    # next step: create a KML with icons to be used with oruxmaps

    kml = simplekml.Kml(name="<![CDATA["+brand_or_name+"]]>", visibility = "1" , open ="1", atomauthor = "Hans Straßgütl" , atomlink = "https://gravelmaps.de"  )  
    for element in coords:
        pt2 = kml.newpoint(name='<![CDATA[' + element["name"] + ']]>',coords=[(element["lon"], element["lat"])], description = element["description"] )
        pt2.style.iconstyle.icon.href = orux_icon
    kml.save(kml_orux_name)                                                 # Now the OruxMaps KML is saved.

    rework_kml_for_organic(kml_organic_name, organic_color)                

    copy_path = ".\\POI_ww\\"
    if not os.path.exists(copy_path): os.mkdir(copy_path)                                                        
    shutil.copy2(gpx_name , copy_path+gpx_name)                             
    os.remove(gpx_name)                                                     
    shutil.copy2(gpi_name , copy_path+gpi_name)                             
    os.remove(gpi_name)                                                     
    # shutil.copy2(kml_name , copy_path+kml_name)                             
    os.remove(kml_name)                                                     
    shutil.copy2(kml_orux_name , copy_path+kml_orux_name)                
    os.remove(kml_orux_name)                                               
    shutil.copy2(kml_organic_name , copy_path+kml_organic_name)             
    os.remove(kml_organic_name)                                             
    

# -----------------------------------------------------------------------------------------
#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    os.system('cls') 
    # ....................................................
    # Erhalte die Übergabeparameter. Erstelle dazu den 
    # default GPX Entry - sofern übergeben.
    # Ansonsten setze Default Pfad auf den Pfad der Exe
    # 
    #  Der Übergabe Paramater MUSS so aussehen: 
    # --dictionary "{'key':'tourism', 'tag':'alpine_hut', 'clear_name':'Alpine_Hut', 'icon':'Alpinehut.svg', 'icon_color':'placemark-brown','brand':'false', 'brand_name':'', 'second_key':'', 'second_tag':'' }"
    # ....................................................
    # os.system('cls') 
    my_script = h_utils.IchSelbst()
    my_name = sys.argv[0]                       # the first argument is the script itself
    file_paths = sys.argv[1:]                   # the first argument (0) is the script itself. 1: heisst, wir haben nun in der file_paths alle anderen Argumente
    # ....................................................
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print("\n\tPull data from Overpass Turbo and convert it.\n\t\tVersion v1 dated 11/2024\n\t\tWritten by Hans Strassguetl - https://gravelmaps.de \n\t\tLicenced under https://creativecommons.org/licenses/by-sa/4.0/ \n\t\tIcons used are licensed under: Map Icons Collection - Creative Commons 3.0 BY-SA\n\t\tAuthor: Nicolas Mollet - https://mapicons.mapsmarker.com\n\t\tor https://creativecommons.org/publicdomain/zero/1.0/deed.en\n\n")
    # .......................................................................
    # Some basic definitions
    # .......................................................................
    GPSBabel = "C:\\Program Files\\GPSBabel\\GPSBabel.exe"
    # .......................................................................
    # Build of overpass query for GasGas
    # .......................................................................
    # Define the variable
    brand_or_name = "GENERIC"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "BMW"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "GasGas"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "Husqvarna"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "CFMOTO"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "CF MOTO"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "Honda"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "Yamaha"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")
    brand_or_name = "Suzuki"
    make_gpx_gpi(brand_or_name,"ATV","placemark-orange")

    