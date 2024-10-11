import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_charts():
    if os.path.exists('survey_results.csv'):
        df = pd.read_csv('survey_results.csv', header=None, names=['Genre', 'ListeningTime'])

        # Count occurrences of each genre
        genre_counts = df['Genre'].value_counts()

        # Count occurrences of each listening time
        listening_time_counts = df['ListeningTime'].value_counts()

        # Create a figure for the charts
        fig, axes = plt.subplots(1, 2, figsize=(26.25, 11.25))

        # Plot pie chart for genres
        genre_counts.plot.pie(autopct='%1.1f%%', startangle=140, cmap='tab20', ax=axes[0])
        axes[0].set_title('Favorite Music Genres', fontsize=24)
        axes[0].set_ylabel('')  # Hide the y-label

        # Plot bar chart for listening time
        listening_time_counts.plot.bar(color='skyblue', ax=axes[1])
        axes[1].set_title('Listening Time per Day', fontsize=24)
        axes[1].set_xlabel('Listening Time (hours)', fontsize=18)
        axes[1].set_ylabel('Number of Responses', fontsize=18)
        axes[1].set_xticks(range(len(listening_time_counts)))
        axes[1].set_xticklabels(listening_time_counts.index, rotation=0, fontsize=12)

        # Save the figure
        fig.savefig('static/charts.png')
        plt.close(fig)