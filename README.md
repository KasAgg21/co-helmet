# Helmet System for Coal Mines - Software Documentation

## Overview

This repository contains the Python software component for a safety helmet system designed for coal miners. The software handles data acquisition from the helmet sensors, processes it, and displays real-time statistics on a dashboard. It is designed to work in conjunction with custom hardware that includes various sensors and communication modules.

## Features

- **Real-Time Data Visualization:** Graphically displays carbon monoxide levels and helmet wear status.
- **Serial Communication:** Communicates with the helmet via serial port to receive sensor data.
- **Database Management:** Stores sensor data in a SQLite database for historical analysis.
- **Alert System:** Issues visual and audio alerts when carbon monoxide levels exceed safe thresholds.
- **Data Export:** Allows exporting of collected data to Excel for further analysis.

## Prerequisites

Before running the Python script, ensure you have the following installed:
- Python 3.x
- pandas
- matplotlib
- sqlite3
- tkinter

You can install the necessary libraries using pip:
```bash
pip install pandas matplotlib sqlite3
```

## Getting Started

Clone the repository and navigate to the software directory:

```bash
Copy code
git clone https://github.com/yourgithubusername/helmet-system.git
cd helmet-system/software
```

## Running the Application

To run the dashboard application, execute:
```
bash
Copy code
python dashboard.py
```

## Usage Instructions

Connect to Helmet:
Click the "Connect to Helmet" button to establish a serial connection with the helmet.
Ensure the correct COM port is set in the script.

## Monitoring:

The dashboard will display real-time updates of CO levels and whether the helmet is currently worn.
Alerts are visually displayed if CO levels exceed the predefined safe threshold.

## Data Export:

Use the "Export to Excel" button to save the collected data to an Excel file for offline analysis.

## Software Structure

dashboard.py: Main script for running the graphical user interface.
sensor_data.db: SQLite database file for storing sensor readings.
helmet_data.xlsx: Default output file for data export.
