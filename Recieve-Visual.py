import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial  # Import serial library
import time

# Initialize global variables
connected = False
co_threshold = 600  # Example threshold for CO level
times = []
co_levels = []
start_time = time.time()
alert_played = False

# Set up the serial connection
try:
    ser = serial.Serial('COM3', 9600, timeout=1)  # Update the COM port as necessary
except:
    messagebox.showerror("Serial Connection Error", "Unable to connect to the helmet via serial port.")

# Set up SQLite database
conn = sqlite3.connect('helmet_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
             co_level INTEGER,
             helmet_worn BOOLEAN)''')
conn.commit()

# Create the main application window
root = tk.Tk()
root.title("Helmet Monitoring Dashboard")

# Create global references for Tkinter widgets
connection_status_label = tk.Label(root, text="Not Connected", fg="red")
wearing_status_label = tk.Label(root, text="Wearing Status: Unknown", fg="black", font=("Helvetica", 14))
warning_label = tk.Label(root, text="CO level status: Unknown", fg="black", font=("Helvetica", 14))

def connect_helmet():
    global connected
    if ser.is_open:
        connected = True
        connection_status_label.config(text="Connected", fg="green")
        start_data_collection()
    else:
        messagebox.showerror("Error", "Serial connection not available.")

def start_data_collection():
    if not connected:
        messagebox.showerror("Error", "Not connected to the helmet!")
        return
    
    ani.event_source.start()

def insert_data(co_level, helmet_worn):
    c.execute("INSERT INTO sensor_data (co_level, helmet_worn) VALUES (?, ?)", (co_level, helmet_worn))
    conn.commit()

def update(frame):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split(',')
        if len(data) == 2:
            co_level = float(data[0].split(': ')[1])
            helmet_worn = bool(int(data[1].split(': ')[1]))

            insert_data(co_level, helmet_worn)

            # Update data lists
            times.append(time.time() - start_time)
            co_levels.append(co_level)

            # Trim lists to last 10 readings for real-time effect
            times_trimmed = times[-10:]
            co_levels_trimmed = co_levels[-10:]

            # Update plot
            line.set_data(times_trimmed, co_levels_trimmed)
            ax.set_xlim(min(times_trimmed), max(times_trimmed) + 1)

            # Update status labels
            wearing_status_label.config(text="Worn" if helmet_worn else "Not Worn", fg="green" if helmet_worn else "red")
            if co_level > co_threshold:
                warning_label.config(text="WARNING: High CO level!", fg="red")
            else:
                warning_label.config(text="CO level normal", fg="green")

    return line,

def export_to_excel():
    try:
        df = pd.read_sql_query("SELECT * FROM sensor_data", conn)
        file_path = "helmet_data.xlsx"
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Failed", str(e))

def close_application():
    # Ask for confirmation before closing
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Close the Tkinter window
        conn.close()  # Close the SQLite connection
        ser.close()  # Close the serial connection

# Set up the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-', lw=2)
ax.set_xlim(0, 10)
ax.set_ylim(0, 1024)  # Assuming a 10-bit ADC for CO sensor

ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)  # Update interval shortened to 1 second
ani.event_source.stop()  # Start animation only when connected

# Connection button
connection_button = tk.Button(root, text="Connect to Helmet", command=connect_helmet)
connection_button.pack(pady=10)

# Export to Excel button
export_button = tk.Button(root, text="Export to Excel", command=export_to_excel)
export_button.pack(pady=10)

# Close button
close_button = tk.Button(root, text="Close", command=close_application)
close_button.pack(pady=10)

# Connection status label
connection_status_label.pack(pady=5)

# Graph display
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Helmet wearing status
wearing_status_label.pack(pady=10)

# CO level warning status
warning_label.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()

# Close the SQLite connection when done
conn.close()
