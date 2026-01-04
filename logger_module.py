# logger_module.py
import csv
import os
import ac
import datetime

# convert time to seconds
def ac_time_to_seconds(time_str):
    try:
        if not time_str or "-" in time_str:
            return None
        parts = time_str.split(":")
        if len(parts) == 3:
            minutes = float(parts[0])
            seconds = float(parts[1])
            milliseconds = float(parts[2])
            return minutes*60 + seconds + milliseconds/1000
        elif len(parts) == 2:
            seconds = float(parts[0])
            milliseconds = float(parts[1])
            return seconds + milliseconds/1000
        else:
            return float(parts[0])
    except Exception as e:
        ac.log("Time conversion error: " + str(e))
        return None

# convert to AC time format MM:ss.mmm
def seconds_to_ac_format(seconds):
    if seconds is None:
        return ""
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return "{}{}:{:02d}.{:03d}".format(sign, minutes, sec, ms)

# tire life calculation
def tyre_life_from_distance(distance_km):
    MAX_DIST = 224.4

    if distance_km <= 0:
        return 100.0
    if distance_km >= MAX_DIST:
        return 0.0

    life = 100.0 * (1.0 - distance_km / MAX_DIST)
    return round(life, 3)

# create data folder
def ensure_data_folder():
    # Documents/Assetto Corsa/apps/Log-ger/data
    documents = os.path.expanduser("~\\Documents")
    ac_folder = os.path.join(documents, "Assetto Corsa", "apps", "Log-ger", "data")
    if not os.path.isdir(ac_folder):
        os.makedirs(ac_folder)
    return ac_folder

# get curr date
def get_date():
    now = datetime.datetime.now()
    return "{:02d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
        now.day, now.month, now.year % 100,
        now.hour, now.minute, now.second
    )

# create unique filename
def build_csv_filename(track_name, car_model):
    safe_track = track_name.lower().replace(" ", "_")
    safe_car = car_model.lower().replace(" ", "_")
    date_str = get_date()
    return safe_track + "-" + safe_car + "-" + date_str + ".csv"

class LapLogger:
    def __init__(self, track_name, car_model):
        # folder path
        data_folder = ensure_data_folder()

        # file path
        self.filename = os.path.join(
            data_folder,
            build_csv_filename(track_name, car_model)
        )

        # initialize variables
        self.last_completed_lap = -1
        self.previous_lap_seconds = None
        self.best_lap_seconds = None
        self.fuel_at_lap_start = None
        self.total_distance = 0.0
        self.tyre_wear = 100.0

    def log_lap(self, lap_number, lap_time, best_time, fuel, track_km):
        # lap number check
        if lap_number <= self.last_completed_lap:
            return
        self.last_completed_lap = lap_number

        # change lap format
        lap_sec = ac_time_to_seconds(lap_time)
        best_sec = ac_time_to_seconds(best_time)

        # delta_prev calculation
        delta_prev = ""
        if lap_sec is not None and self.previous_lap_seconds is not None:
            delta_prev = lap_sec - self.previous_lap_seconds

        # delta_best calculation
        delta_best = ""
        if lap_sec is not None and self.best_lap_seconds is not None:
            delta_best = lap_sec - self.best_lap_seconds

        # best_lap calculation
        self.previous_lap_seconds = lap_sec
        if best_sec is not None:
            if self.best_lap_seconds is None or best_sec < self.best_lap_seconds:
                self.best_lap_seconds = best_sec

        # fuel_used calculation
        fuel_used = ""
        if self.fuel_at_lap_start is not None:
            fuel_used = round(self.fuel_at_lap_start - fuel, 3)

        # tyre_wear calculation
        self.total_distance = track_km
        tyre_wear = tyre_life_from_distance(self.total_distance)
        
        # fuel update
        self.fuel_at_lap_start = fuel

        ac.log("distance km:" + str(self.total_distance) + " tyre_wear:" + str(tyre_wear))
        # write to file
        file_exists = os.path.isfile(self.filename)
        try:
            with open(self.filename, mode="a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow([
                        "lap_number",
                        "lap_time",
                        "best_time",
                        "delta_best",
                        "delta_prev",
                        "fuel_used",
                        "fuel_left",
                        "est_tyre_wear"
                    ])
                writer.writerow([
                    lap_number,
                    seconds_to_ac_format(lap_sec),
                    seconds_to_ac_format(best_sec),
                    seconds_to_ac_format(delta_best) if delta_best != "" else "",
                    seconds_to_ac_format(delta_prev) if delta_prev != "" else "",
                    fuel_used,
                    round(fuel, 3),
                    tyre_wear
                ])
                csvfile.close()
        except Exception as e:
            ac.log("LapLogger error: " + str(e))