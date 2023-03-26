from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import librosa
import librosa.display
import IPython.display as ipd
import multiprocessing as mp
import time
import os
from glob import glob
from pathlib import Path
from datasketch import MinHash, MinHashLSH, MinHashLSHForest


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    file_path = request.form['file_path']
    # Do something with file_path
    df = pd.read_csv("C:\\Users\\Farhan\\Desktop\\pycharm projects\\mfcc_feature.csv")
    arr1 = df.values

    def find_nearest_neighbors(df_, to_check):  # , jaccard_threshold=0.5):
        # Create an instance of MinHash with the given number of permutations
        num_permutations = 100
        band_width = 10
        num_neighbors = 10
        minhash = MinHash(num_perm=num_permutations)

        lsh = MinHashLSHForest(num_perm=num_permutations, l=band_width)

        # Counter for the index of the data
        counter = 0

        # Loop through the rows of the dataframe and update the MinHash object for each column value
        for i in df_.index:
            # Create a new MinHash object for each row
            minhash = MinHash(num_perm=num_permutations)
            for j in df_.iloc[i]:
                # Update the MinHash object with the string representation of the column value
                minhash.update(str(j).encode('utf8'))
            # Add the MinHash object to the LSH Forest with a unique label
            lsh.add("data point " + str(counter), minhash)
            # Increment the counter
            counter += 1

        # Build the index for the LSH Forest
        lsh.index()

        # Create a new MinHash object for the query data
        query_minhash = MinHash(num_perm=num_permutations)

        # Loop through the query data and update the MinHash object for each value
        query_data = df.iloc[4]
        #query_data = to_check
        for j in query_data:
            query_minhash.update(str(j).encode("utf8"))

        # Query the LSH Forest for the nearest neighbors to the query MinHash object with Jaccard similarity greater than jaccard_threshold
        query_result_ = lsh.query(query_minhash, num_neighbors)

        # Return the query result
        return query_result_

    mfcc_new = []
    # C:\Users\Farhan\Desktop\Semester 4\Big Data Theory\testing_audios\0_01_0.wav
    #file_path = input("Path:")
    x, sample_rate = librosa.load(path=file_path, res_type='kaiser_fast')  # ,res_type='kaiser_fast'
    mfccs = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=50, lifter=100).T, axis=0)
    mfcc_new.append(mfccs)
    mfcc_new = pd.DataFrame(mfcc_new)
    query_result = find_nearest_neighbors(df,mfcc_new)  # , num_permutations=100, band_width=5, num_neighbors=5)#, jaccard_threshold=0.5)

    # Print the result
    output = str()
    if not query_result:
        output = "No match found"
    else:
        output = "Approximate nearest neighbors with Jaccard similarity >0.5:" + str(query_result)
    return render_template('play.html', file_path=output)

if __name__ == '__main__':
    app.run(debug=True)
