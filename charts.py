import tkinter as tk
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
        genre_counts.plot.pie(autopct='%1.1f%%', startangle=140, ax=axes[0])
        axes[0].set_title('Favorite Music Genres')

        # Plot bar chart for listening time
        listening_time_counts.plot.bar(ax=axes[1])
        axes[1].set_title('Listening Time per Day')
        axes[1].set_xlabel('Listening Time (hours)')
        axes[1].set_ylabel('Number of Responses')

        # Draw the updated plots
        canvas.draw()

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

# Add the IP address label to the frame
ip_label = tk.Label(ip_frame, text=f"Local IP: {local_ip}", font=("Helvetica", 24), bg="white")
ip_label.pack(pady=10)

# Generate and display the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(f"http://{local_ip}:3000")
qr.make(fit=True)
qr_img = qr.make_image(fill='black', back_color='white')
qr_img = qr_img.resize((200, 200), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
qr_photo = ImageTk.PhotoImage(qr_img)
qr_label = tk.Label(ip_frame, image=qr_photo, bg="white")
qr_label.pack(pady=10)

# Create a frame to hold the charts
chart_frame = tk.Frame(root, bg="white")
chart_frame.pack(pady=30)

# Create a figure for the charts
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Create a canvas to display the figure
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack()

# Update the charts initially
update_charts()

# Schedule the chart updates
def refresh_charts():
    update_charts()
    root.after(5000, refresh_charts)  # Refresh every 5 seconds

refresh_charts()

# Start the Tkinter main loop
root.mainloop()

# Terminate the server process when the Tkinter window is closed
if server_process:
    server_process.terminate()
