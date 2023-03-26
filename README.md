# Flask-Web-App-for-Finding-Similar-Songs-using-LSH

This is a simple Flask application that allows you to analyze the similarity between your music files based on their MFCC (Mel-Frequency Cepstral Coefficients) features.

## Installation
-Clone this repository to your local machine.
-Install the required dependencies using pip:
-pip install flask pandas numpy librosa datasketch

## Usage
-Navigate to the project directory in your terminal.
-Run the Flask app using the command:
`python3 app.py`
-Open your web browser and go to http://localhost:5000.
-Click the "Choose File" button and select a music file to analyze.
-Click the "Analyse" button to analyze the selected file.
-The application will return a list of approximate nearest neighbors with Jaccard similarity >0.5 based on their MFCC features.

## Libraries
This application was created using the following libraries:

-Flask
-Pandas
-NumPy
-LibROSA
-DataSketch

## Collaborators
Faizan Ahmad
Muhammad Farhan
