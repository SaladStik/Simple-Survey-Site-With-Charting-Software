import os
import time
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def kill_port(port):
    import psutil
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    proc.kill()
                    print(f"Killed process {proc.pid} using port {port}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

@app.route('/')
def index():
    return render_template('survey.html')

@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    genre = request.form.get('genre')
    listening_time = request.form.get('listening-time')
    
    if not genre or not listening_time:
        return "Invalid input", 400
    
    # Save the survey result to CSV
    with open('./output/survey_results.csv', 'a') as f:
        f.write(f"{genre},{listening_time}\n")
    
    return redirect(url_for('view_charts'))

@app.route('/chart-data')
def chart_data():
    if os.path.exists('./output/survey_results.csv'):
        df = pd.read_csv('./output/survey_results.csv', header=None, names=['Genre', 'ListeningTime'])

        # Count occurrences of each genre
        genre_counts = df['Genre'].value_counts().to_dict()

        # Count occurrences of each listening time
        listening_time_counts = df['ListeningTime'].value_counts().to_dict()

        return jsonify({
            'genre_counts': genre_counts,
            'listening_time_counts': listening_time_counts
        })
    else:
        return jsonify({
            'genre_counts': {},
            'listening_time_counts': {}
        })

@app.route('/view-charts')
def view_charts():
    return render_template('charts.html')

if __name__ == '__main__':
    kill_port(3000)  # Ensure port 3000 is free
    app.run(host='0.0.0.0', port=3000)