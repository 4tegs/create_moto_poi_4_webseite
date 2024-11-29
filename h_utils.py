
from pathlib import Path
import json
import gpxpy
import os
import sys
from tkinter import * # type: ignore
from tkinter import ttk
from ttkthemes import ThemedTk
import xml.etree.ElementTree as ET
import keyboard

# ------------------------------------------------------------------------------------------
#  _____                         
# | ____|_ __ _ __ ___  _ __ ___ 
# |  _| | '__| '__/ _ \| '__/ __|
# | |___| |  | | | (_) | |  \__ \
# |_____|_|  |_|  \___/|_|  |___/
# ------------------------------------------------------------------------------------------
def error_message(error, quit):
    ''' Error Section. Hand over error-level. Program will be quit. '''
    
    def exit_now():
        if quit:
            sys.exit('Oh weh - ein Fehler!')
        else:
            root.destroy()

    # root = Tk()
    root = ThemedTk(theme='radiance')
    root.title("Error!!")
    root.eval('tk::PlaceWindow . center')

    mainframe = ttk.Frame(root, padding="25 25 25 25")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))            # type: ignore
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    quitbutton = ttk.Button(mainframe, text='Exit', command=exit_now)
    quitbutton.grid(column=1, row=4, sticky="S")


    # .............................................................
    # JSON Errors
    # .............................................................
    if error == "json_01":
        ttk.Label(mainframe, text="The configuration (JSON) is missing.").grid(column=1, row=1, sticky=W)
    if error == "json_02":
        ttk.Label(mainframe, text="The configuration (JSON) is missing.\nTry to get the default one.\nRead Readme on Github!").grid(column=1, row=1, sticky=W)
    # .............................................................
    # GPX Errors
    # .............................................................
    if error == "gpx_01":
        ttk.Label(mainframe, text="No GPX FileName has been passed. Use drag & drop.").grid(column=1, row=1, sticky=W)
    if error == "gpx_02":
        ttk.Label(mainframe, text="Wrong FileType has been provided to work on. Must be GPX.").grid(column=1, row=1, sticky=W)
    if error == "gpx_03":
        ttk.Label(mainframe, text="There is a mix of standard GPX and Garmin GPX in this file. That doen't work. Fix it.").grid(column=1, row=1, sticky=W)
    if error == "gpx_04":
        ttk.Label(mainframe, text="There is no such GPX file!\nUse drag & drop.").grid(column=1, row=1, sticky=W)

    # .............................................................
    # Paramater passing Errors
    # .............................................................
    if error == "dict_01":
        ttk.Label(mainframe, text="Error: The --dictionary argument is required.").grid(column=1, row=1, sticky=W)
    if error == "dict_02":
            ttk.Label(mainframe, text="Error: Unable to parse the dictionary argument provided by you.").grid(column=1, row=1, sticky=W)
    if error == "dict_03":
            ttk.Label(mainframe, text="Esssential JSON parameter in the command line is missing.").grid(column=1, row=1, sticky=W)
    if error == "dict_04":
            ttk.Label(mainframe, text="Country wasn't found in translation table from country-name to ISO code.").grid(column=1, row=1, sticky=W)
    
    if error == "7z_01":
            ttk.Label(mainframe, text="7Z Program missing.").grid(column=1, row=1, sticky=W)
    if error == "GPSBabel":
            ttk.Label(mainframe, text="GPSBabel Program missing. Necessary to create Garmin POI.").grid(column=1, row=1, sticky=W)

    # .............................................................
    # Traccar Errors
    # .............................................................
    if error == "traccar_1":
        ttk.Label(mainframe, text="The configuration <traccar2gpx.json> is missing.").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="A new version has been created ").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="YOU MUST UPDATE the created version with your credentials before you can carry on!").grid(column=1, row=3, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    quitbutton.focus()
    root.mainloop()

# -------------------------------------------------------------
#  ____  _             _     ____            _       _     
# / ___|| |_ __ _ _ __| |_  / ___|  ___ _ __(_)_ __ | |_ 
# \___ \| __/ _` | '__| __| \___ \ / __| '__| | '_ \| __|
#  ___) | || (_| | |  | |_   ___) | (__| |  | | |_) | |_ 
# |____/ \__\__,_|_|   \__| |____/ \___|_|  |_| .__/ \__|
#                                             |_|        
#  ____                                _            
# |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ 
# | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__|
# |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |   
# |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|   
# -------------------------------------------------------------
class IchSelbst:
    '''
    Make Names from running Script.
    sys.argv[0] zeigt, wenn man die py laufen lässt, auf den Python Interpreter bzw. die py.
    Sobald die py zur Exe wird zeigt der Pfad zur Working Directory des Callers, also des GPX das ich Droppe. 
    Damit müsste immer dort wo die GPX liegt auch die JSON liegen. 
    sys.executable ist der Workaround. 
    Mehr dazu hier: https://pyinstaller.org/en/stable/runtime-information.html 

    self.script_with_path           ->  c:\\SynologyDrive\\Python\\00_test\\test2.py
    self.script                     ->  test2.py
    self.name                       ->  test2
    self.path                       ->  c:\\SynologyDrive\\Python\\00_test
    self.path_name_without_suffix   ->  c:\\SynologyDrive\\Python\\00_test\\test2
    '''
    def __init__(self):
        if getattr(sys, 'frozen', False):                                   # Code is running from a compiled executable
            SysArg0  = sys.executable
        else:                                                               # Code is running as a regular Python script
            SysArg0 = sys.argv[0]

        self.script_with_path           = SysArg0                               # Script mit vollem Path
        self.script_with_suffix         = Path(SysArg0).name                    # Der Dateiname mit Suffix
        self.script_without_suffix      = Path(SysArg0).stem                    # Das ist der DateiName OHNE Suffix
        self.path                       = Path(SysArg0).parent                  # Das ist der Path ohne trailing \
        self.path_name_without_suffix   = str(Path(SysArg0).parent) + "\\" + Path(SysArg0).stem
        # ----------------------------------------------------------------------------------------
        # Here comes some code that maybe used in case the JSON file is included in the EXE file. 
        # ----------------------------------------------------------------------------------------
        if getattr(sys, 'frozen', False):                                   # Code is running from a compiled executable
            try:
                base_path = sys._MEIPASS                                    # type: ignore
            except AttributeError:
                base_path = os.path.abspath(".")
            # By compiling the JSON into the package, the path uses the name of the JSON as a subfolder, 
            # for that the Path(SysArg0).stem var needs to be added twice
            self.data_file = base_path + "\\" + Path(SysArg0).stem + ".json\\" + Path(SysArg0).stem 
        else:
            self.data_file = self.path_name_without_suffix
        # ----------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------
#      _ ____   ___  _   _ 
#     | / ___| / _ \| \ | |
#  _  | \___ \| | | |  \| |
# | |_| |___) | |_| | |\  |
#  \___/|____/ \___/|_| \_|
# ------------------------------------------------------------------------------------------
def load_json(json_file_name):
# ------------------------------------------------------------------------------------------
# Load Translation Table 
# 2024 02 04
# ------------------------------------------------------------------------------------------
    ''' If exists: Load JSON file. -> JSON  '''
    my_script = IchSelbst()
    if json_file_name == None:
        json_file_name = my_script.path_name_without_suffix+".json"

    try:											
        with open(json_file_name) as f:				
            return json.load(f)						
    except FileNotFoundError:
        json_file_name = my_script.data_file+".json"
        try:
            error_message("json_02", False)
            with open(json_file_name) as f:				
                return json.load(f)						
        except:
            error_message("json_01", False)
            sys.exit(1)

# ------------------------------------------------------------------------------------------
#   ____                      _            ____                 _       _ 
#  / ___| __ _ _ __ _ __ ___ (_)_ __      / ___| _ __   ___ ___(_) __ _| |
# | |  _ / _` | '__| '_ ` _ \| | '_ \ ____\___ \| '_ \ / _ \_  / |/ _` | |
# | |_| | (_| | |  | | | | | | | | | |_____|__) | |_) |  __// /| | (_| | |
#  \____|\__,_|_|  |_| |_| |_|_|_| |_|    |____/| .__/ \___/___|_|\__,_|_|
#                                               |_|                       
# ------------------------------------------------------------------------------------------
def read_garmin_DisplayColor(gpx_file_path):
    ''' 
    Ich lese den GPX Track per XML Parser ein, lese die DisplayColors aus und übergebe diese 
    in einer Liste: display_colors
    '''
    # ....................................................
    # Spezialbehandlung für den GPX Track!
    # Ich hole die DisplayColor aus dem GPX Track. GPXPY kann keine Garmin codes lesen! 
    # Die alte Bibliothek gpxdata, obwohl sie eigentlich passen müsste, liess sich nicht mehr nutzen.
    # Ich habe Stunden damit zugebracht die Garmin Struktur ansprechen zu können. NUR dieser Weg ging bislang!
    # Also jede einzelne Elementstruktur in der Tiefe der GPX / XML mit ihrem Namespace ansprechen.
    # So zerlegt sich das: 
    #   <gpx creator="Garmin........                                          = . = root
    #         <trk>                                                           = ./h_main:trk/
    #              <name>Track 005</name>                                      
    #              <extensions>                                               = ./h_main:trk/h_main:extensions
    #                 <gpxx:TrackExtension>                                   = ./h_main:trk/h_main:extensions/h_gpxx:TrackExtension
    #                     <gpxx:DisplayColor>DarkGray</gpxx:DisplayColor>     = ./h_main:trk/h_main:extensions/h_gpxx:TrackExtension/h_gpxx:DisplayColor
    #                 </gpxx:TrackExtension>
    #             </extensions>
    #         <trkseg>....
    #     </gpx>
    # ....................................................
    tree = ET.parse(gpx_file_path)
    root = tree.getroot()
    ns = {'h_main': 'http://www.topografix.com/GPX/1/1' ,
        'h_gpxx': 'http://www.garmin.com/xmlschemas/GpxExtensions/v3'}
    display_colors = root.findall("./h_main:trk/h_main:extensions/h_gpxx:TrackExtension/h_gpxx:DisplayColor", ns)
    return display_colors


def read_gpx(file_path):
    '''
    Receive the name of the GPX file. 
    Return a parsed GPX and the colors of the tracks if there are any.
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as gpx_file:    # Parse die GPX mit dem Standard gpxpy
            gpx_data = gpx_file.read()
        gpx = gpxpy.parse(gpx_data)
    except FileNotFoundError:
        error_message("gpx_04", True)
    
    display_colors = read_garmin_DisplayColor(file_path)        # Hole die Garmin Trackfarben als Speziallösung weil gpxpy die nicht lesen kann!    
    # prüfe ob du nicht einen Mix aus normalen und Garmin Tracks hast. Das geht sonst nicht, weil ich nie weiß, wo die Farben sitzten.
    if len(display_colors) >0 and (len(display_colors) != len(gpx.tracks)):
        error_message("gpx_03", True)
    return gpx, display_colors

def make_gpx_name(gpx_in_file_name):
# ...................................................
# Make GPX FileName
# 2022 12 06
# ...................................................
    '''
    Make a valid GPX name

    ### Args: 
    - Input  : GPX File Name to be analyzed
    - Returns: GPX File Name to be used. May be blank
    '''
    if gpx_in_file_name == None:
        if len(sys.argv[1:]) > 0:
            file_paths = sys.argv[1:]                   # the first argument (0) is the script itself. 1: heisst, wir haben nun in der file_paths alle anderen Argumente
            gpx_in_file_name = file_paths[0]
        else: 
            error_message("gpx_01", True)
    
    if gpx_in_file_name:
        in_path = Path(gpx_in_file_name).parent     # Der Pfad zur EingabeDatei
        in_name = Path(gpx_in_file_name).stem       # Der Name der Datei ohne Suffix
        in_suffix = Path(gpx_in_file_name).suffix    
        if in_suffix.lower() != '.gpx':         # Prüfe ob das richtige Datenformat eingegeben wurde
            # in_name = ""                            # Wenn falsch, dann kein EingabeName
            # in_suffix = ""                          # Wenn falsch, dann kein EingabeName
            # in_path = my_path                        # Setze den Pfad dieses Programms als Default
            gpx_file_name = ''
        else:
            gpx_file_name = str(in_path) + '\\' + str(in_name) + str(in_suffix)
    else:
        gpx_file_name = ''

    return gpx_file_name

# ------------------------------------------------------------------------------------------
#   ____                _           ____ ______  __
#  / ___|_ __ ___  __ _| |_ ___    / ___|  _ \ \/ /
# | |   | '__/ _ \/ _` | __/ _ \  | |  _| |_) \  / 
# | |___| | |  __/ (_| | ||  __/  | |_| |  __//  \ 
#  \____|_|  \___|\__,_|\__\___|___\____|_|  /_/\_\
#                             |_____|              
# ------------------------------------------------------------------------------------------
def create_gpx_with_symbols(points, output_file, symbol):
    '''
    Create a Garmin-compatible GPX file with waypoints and a specified symbol.

    Args:
        points (list of dict): List of points with 'name', 'lat', and 'lon'.
        output_file (str): Path to the output GPX file.
        symbol (str): The symbol to use for all waypoints.
    '''
    # Create the root element
    gpx = ET.Element("gpx", xmlns="http://www.topografix.com/GPX/1/1", version="1.1", creator="PythonScript")
    
    # Add waypoints with the specified symbol
    for point in points:
        wpt = ET.SubElement(gpx, "wpt", lat=str(point["lat"]), lon=str(point["lon"]))
        name = ET.SubElement(wpt, "name")
        name.text = point["name"]
        sym = ET.SubElement(wpt, "sym")
        sym.text = symbol  # Use the provided symbol for all waypoints
    
    # Write the GPX file
    tree = ET.ElementTree(gpx)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# ------------------------------------------------------------------------------------------
#   ____                      _         ___           _                  
#  / ___| __ _ _ __ _ __ ___ (_)_ __   |_ _|_ __  ___| |_ __ _ _ __  ____
# | |  _ / _` | '__| '_ ` _ \| | '_ \   | || '_ \/ __| __/ _` | '_ \|_  /
# | |_| | (_| | |  | | | | | | | | | |  | || | | \__ \ || (_| | | | |/ / 
#  \____|\__,_|_|  |_| |_| |_|_|_| |_| |___|_| |_|___/\__\__,_|_| |_/___|
# ------------------------------------------------------------------------------------------
class mein_gpx:
    '''
    Input:  Entweder ein validierter Name für die GPX Datei, oder None
            Mit None holt er sich den ersten Parameter der mitgegeben wurde (Drag & Drop)
    Output: Eine Instanz mit dem Namen des GPX, allen GPX Daten fertig geparsed, die Farben der Tracks sofern vorhanden.
    '''
    def __init__(self, gpx_in_file_name):
        if gpx_in_file_name == None:
            if len(sys.argv[1:]) > 0:
                gpx_in_file_name = sys.argv[1:][0]
            else: 
                error_message("gpx_01", True)
        
        self.gpx_name_with_path = make_gpx_name(gpx_in_file_name)
        self.gpx, self.display_color = read_gpx(self.gpx_name_with_path)
        
        SysArg0 = self.gpx_name_with_path                                           # Der komplete Pfad mit Dateinamen und Suffix
        self.gpx_name_with_suffix           = Path(SysArg0).name                    # Nur der Dateiname mit Suffix
        self.gpx_name_without_suffix        = Path(SysArg0).stem                    # Nur der DateiName OHNE Suffix
        self.gpx_path_name_without_suffix   = Path(SysArg0).parent                  # Das ist der Path ohne trailing \
        self.gpx_path_with_name_no_suffix   = str(Path(SysArg0).parent) + "\\" + Path(SysArg0).stem #  Der Pfad mit Dateinamen aber ohne den Suffix
        
# ------------------------------------------------------------------------------------------
#  _____ _ _          _                     _ _ _             
# |  ___(_) | ___    | |__   __ _ _ __   __| | (_)_ __   __ _ 
# | |_  | | |/ _ \   | '_ \ / _` | '_ \ / _` | | | '_ \ / _` |
# |  _| | | |  __/   | | | | (_| | | | | (_| | | | | | | (_| |
# |_|   |_|_|\___|___|_| |_|\__,_|_| |_|\__,_|_|_|_| |_|\__, |
#               |_____|                                 |___/ 
# ------------------------------------------------------------------------------------------
def make_short_name(in_file_name , in_suffix ):
# ...................................................
# Make Short and Temp FileName
# Only Name - no path
# 2024 11 19
# ...................................................
    '''
    Make a valid KML name, only name and suffix, no path

    ### Args: 
    - Input  :  File Name to be analyzed
    - Returns:  File Name to be used. May be blank
                Temp Name
    '''
    if in_file_name:
        in_name = Path(in_file_name).stem      # Der Name der Datei ohne Suffix
        short_file_name = str(in_name) + '.' + in_suffix
        tmp_file_name = str(in_name) + '_tmp' + '.' + in_suffix
    else:
        short_file_name = ''
        tmp_file_name = '1q2w3e4r5t.txt'
    return short_file_name , tmp_file_name






