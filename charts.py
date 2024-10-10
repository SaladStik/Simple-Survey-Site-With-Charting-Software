import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket
import os
import subprocess
import psutil
import qrcode
from PIL import Image, ImageTk
import time

# Global variable to store the server process
server_process = None


# Function to get the local IP address
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


# Function to count entries in the CSV file
def count_entries():
    if os.path.exists("./output/survey_results.csv"):
        df = pd.read_csv("./output/survey_results.csv", header=None)
        return len(df)
    return 0


# Function to update the charts
def update_charts():
    if os.path.exists("./output/survey_results.csv"):
        df = pd.read_csv(
            "./output/survey_results.csv", header=None, names=["Genre", "ListeningTime"]
        )

        # Count occurrences of each genre
        genre_counts = df["Genre"].value_counts()

        # Count occurrences of each listening time
        listening_time_counts = df["ListeningTime"].value_counts()

        # Clear previous plots
        for ax in axes:
            ax.clear()

        # Plot pie chart for genres
        genre_counts.plot.pie(
            autopct="%1.1f%%", startangle=140, cmap="tab20", ax=axes[0]
        )
        axes[0].set_title("Favorite Music Genres", fontsize=24)
        axes[0].set_ylabel("")  # Hide the y-label

        # Plot bar chart for listening time
        listening_time_counts.plot.bar(color="skyblue", ax=axes[1])
        axes[1].set_title("Listening Time per Day", fontsize=24)
        axes[1].set_xlabel("Listening Time (hours)", fontsize=18)
        axes[1].set_ylabel("Number of Responses", fontsize=18)
        axes[1].set_xticks(range(len(listening_time_counts)))
        axes[1].set_xticklabels(listening_time_counts.index, rotation=0, fontsize=12)

        # Draw the updated plots
        canvas.draw()

    # Update the counter
    counter_label.config(text=f"Submissions: {count_entries()}")

    # Schedule the next update
    if root.winfo_exists():
        root.after(1000, update_charts)


# Function to close the window
def close_window(event=None):
    global server_process
    root.destroy()
    if server_process:
        server_process.terminate()  # Terminate the server process when closing the window
        server_process.wait()  # Wait for the process to terminate


# Function to check if a port is in use
def is_port_in_use(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False


# Function to kill processes using port 3000
def kill_port_3000_processes():
    command = "for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :3000') do taskkill /f /pid %a"
    for _ in range(2):  # Run the command twice
        subprocess.run(command, shell=True)


# Kill processes using port 3000
kill_port_3000_processes()

# Check if port 3000 is in use
if is_port_in_use(3000):
    print("Port 3000 is already in use. Please free the port and try again.")
    server_process = None
else:
    # Start the Node.js server
    try:
        server_process = subprocess.Popen(
            ["node", "server.js"], cwd=os.path.dirname(os.path.abspath("server.js"))
        )
    except Exception as e:
        print(f"An error occurred while starting the server: {e}")
        server_process = None

# Create the main window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.state("zoomed")  # Maximize the window
root.configure(bg="white")

# Get the local IP address
local_ip = get_local_ip()

# Create a frame to hold the IP label and QR code
ip_frame = tk.Frame(root, bg="white")
ip_frame.pack(pady=30)

# Create and place the IP address label
ip_label = tk.Label(
    ip_frame,
    text=f"Everyone please do the survey at: http://{local_ip}:3000 OR scan this QR Code",
    font=("Helvetica", 36),
    fg="black",
    bg="white",
)
ip_label.pack(side=tk.LEFT, padx=15)

# Generate QR code for the survey URL
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=15,
    border=6,
)
qr.add_data(f"http://{local_ip}:3000")
qr.make(fit=True)
qr_img = qr.make_image(fill="black", back_color="white")
qr_img = qr_img.resize(
    (300, 300), Image.LANCZOS
)  # Use Image.LANCZOS instead of Image.ANTIALIAS
qr_img_tk = ImageTk.PhotoImage(qr_img)

# Create and place the QR code label
qr_label = tk.Label(ip_frame, image=qr_img_tk, bg="white")
qr_label.pack(side=tk.LEFT, padx=15)

# Create and place the counter label at the top
counter_label = tk.Label(
    root,
    text=f"Submissions: {count_entries()}",
    font=("Helvetica", 36),
    fg="black",
    bg="white",
)
counter_label.pack(side=tk.TOP, anchor="n", padx=30, pady=30)

# Create a figure for the charts
fig, axes = plt.subplots(1, 2, figsize=(26.25, 11.25))  # Increased by 25%

# Embed the figure in the tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=30)

# Bind the spacebar key to run the charting software
root.bind("<space>", lambda event: update_charts())

# Bind the Escape key to close the window
root.bind("<Escape>", close_window)

# Start the initial chart update
update_charts()

# Run the main loop
root.mainloop()
