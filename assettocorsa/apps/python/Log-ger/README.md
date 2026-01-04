# Log-ger
**Log-ger** is a lightweight telemetry logger for **Assetto Corsa**, developed by the **Bober Racing Software Development Team.**
The application records **lap-by-lap** data directly from Assetto Corsa’s shared memory and exports it to **clean, Excel-friendly CSV files.**

Log-ger is designed primarily for post-session analysis, allowing comparison of lap times, fuel usage, and tyre wear. It is especially useful for **endurance racing**, such as ACSL Season 7.

## Features:
- Lap-by-lap logging
- CSV export compatible with Excel, LibreOffice, Google Sheets
- Delta calculation:
    - Compared to best lap
    - Compared to previous lap
- Fuel usage per lap
- Remaining fuel after each lap
- Tyre wear calculation for RSS GTM Lanzo V10 based on Hard tyre longevity

Designed for:
- Long stints and endurance runs
- Race analysis
- Post-session review
Runs fully in-game as an Assetto Corsa Python app.

## Default save path:
To maintain clean file management and easy access, all CSV files are saved to:
`C:\Users\<user>\Documents\Assetto Corsa\apps\Log-ger\data`
- A header row is automatically written when a new file is created.
- File name format: 
  `{track_name}-{car_model}-DD-MM-YY-hh-mm-ss.csv`
This ensures:
- Every session has a unique file
- Multiple sessions can be stored without conflicts

Recommended data format in Excel for times:
`[m]:ss.000;-[m]:ss.000` 
This allows proper display of lap times in minutes, seconds, and milliseconds.

## Example Data:
```csv
lap_number,lap_time,best_time,delta_best,delta_prev,fuel_used,fuel_left,tyre_wear
1,1:22.914,,,,0.539,48.341,98.663
2,0:50.985,0:50.985,,-0:31.929,1.209,47.132,97.606
3,0:50.976,0:50.976,-0:00.009,-0:00.009,1.242,45.89,96.556
4,0:50.895,0:50.895,-0:00.081,-0:00.081,1.221,44.669,95.505
5,0:51.155,0:50.895,0:00.260,0:00.260,1.237,43.431,94.453
6,0:50.456,0:50.456,-0:00.439,-0:00.699,1.218,42.214,93.4
7,0:50.353,0:50.456,-0:00.103,-0:00.103,1.201,41.013,92.347
8,0:50.770,0:50.456,0:00.314,0:00.417,1.253,39.76,91.295
9,0:50.252,0:50.252,-0:00.204,-0:00.518,1.244,38.516,90.244
10,0:50.600,0:50.252,0:00.348,0:00.348,1.254,37.262,89.191
```

## Installation:
1) Installation:</br>
    a) Content Manager (CM):</br>
    Drag and drop .zip file on content manager and click install</br>
    b) Assetto Corsa:</br>
    Copy the Log-ger folder into your Assetto Corsa apps folder:</br>
    `Documents\Assetto Corsa\apps\Log-ger`
2) Launch Assetto Corsa and enable Python apps in-game.
3) Start Log-ger from the apps menu.

## Usage:
**Enable Logging:** check the box in the app window </br>
**Open Folder:** opens the data folder in your file explorer </br>
CSV files are automatically created and updated lap-by-lap </br>
**Open .csv file AFTER finishing your current stint!**

## Development Status
This project is **under active development.**
Planned improvements include:
- Improved tyre degradation model
- Stint summaries
- Additional data like:
  - tire temps
  - damage on lap
  - is lap valid
- Additional hud to check which data should be extracted
- Session metadata

## File structure:
```
Log-ger/
│
├─ Log-ger.py        # main app entry point
├─ logger_module.py  # LapLogger and CSV handling
├─ sim_reader.py     # Accesses Assetto Corsa shared memory
└─ third_party/      # ctypes and sim_info that allows to properly extract data from ac session

```

