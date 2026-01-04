import ac
import acsys
import os
import subprocess
from sim_reader import SimReader
from logger_module import LapLogger, ensure_data_folder

# app constants
appName = "Log-ger by BoberRacing"
width, height = 300, 120

# global objects
sim_reader = None
lap_logger = None
appWindow = None
logging_active = False
status_label = None
data_folder_path = None

# checkbox callback
def on_checkbox_changed(name, value):
    global logging_active
    logging_active = True if value == 1 else False

# open folder callback
def on_open_folder(name, value):
    folder = ensure_data_folder()
    if os.path.isdir(folder):
        ac.log("Opening folder: " + folder)
        try:
            import subprocess
            if os.name == "nt":
                subprocess.Popen('explorer "{}"'.format(folder))
            elif os.name == "posix":
                subprocess.Popen(['xdg-open', folder])
        except Exception as e:
            ac.log("Failed to open folder: " + str(e))
    else:
        ac.log("Data folder not found!")

# acMain function
def acMain(ac_version):
    ac.log("Log-ger started")
    global sim_reader, lap_logger, appWindow, status_label
    sim_reader = SimReader()
    lap_logger = None

    # init window
    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)
    ac.drawBorder(appWindow, 0)

    # checkbox
    checkbox = ac.addCheckBox(appWindow, "")
    ac.setPosition(checkbox, 20, 50)
    ac.addOnCheckBoxChanged(checkbox, on_checkbox_changed)
    ac.setFontAlignment(checkbox, "center")

    # label for checkbox
    checkbox_label = ac.addLabel(appWindow, "Enable Logging")
    ac.setPosition(checkbox_label, 50, 50)
    ac.setFontAlignment(checkbox_label, "left")

    # status label
    status_label = ac.addLabel(appWindow, "Status: Disabled")
    ac.setPosition(status_label, 150, 80)
    ac.setFontAlignment(status_label, "center")
    ac.setFontSize(status_label, 16)

    # open folder button
    button_open_folder = ac.addButton(appWindow, "Open 📁")
    ac.setPosition(button_open_folder, 210, 50)
    ac.setSize(button_open_folder, 70, 22)
    ac.addOnClickedListener(button_open_folder, on_open_folder)

    return appName

# update function
def acUpdate(deltaT):
    global sim_reader, lap_logger, logging_active, status_label, data_folder_path

    # update status label
    if status_label:
        if logging_active:
            ac.setFontColor(status_label,0,1,0,1)
            ac.setText(status_label, "Status: Active")
        else:
            ac.setText(status_label, "Status: Disabled")
            ac.setFontColor(status_label,1,0,0,1)

    # gather and log data
    if logging_active and sim_reader:
        track_name = sim_reader.get_track_name()
        car_model = sim_reader.get_car_model()

        if lap_logger is None or lap_logger.filename.find(car_model.lower()) == -1:
            lap_logger = LapLogger(track_name, car_model)
            ac.log("New logger created for track: " + track_name + " car: " + car_model)
            data_folder_path = os.path.dirname(lap_logger.filename)

        lap_number, lap_time, best_time, fuel, track_km = sim_reader.get_lap_data()
        lap_logger.log_lap(lap_number, lap_time, best_time, fuel, track_km)

def acShutdown():
    global sim_reader
    if sim_reader:
        sim_reader.close()
