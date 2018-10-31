import sys
import flask
from flask_debug import Debug
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Initialize our Flask application and the sklearn model
app = flask.Flask(__name__)
model = None

@app.route("/predict", methods=["POST"])
def predict():
    
    # Initialize the data dictionary that will be returned from the view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":    

        # Test data
        input = [[2, 3, 45, 220, 32, 1, 3, 32, 2]]
        prediction = model.predict(input)
        data["prediction"] = {"bug": int(prediction[1:1])}
        
        # indicate that the request was a success
        data["success"] = True
        
    # return the data dictionary as a JSON response
    return flask.jsonify(data)

def train_model():
    # Read in the dataset
    bug_predictor_sample_dataset = pd.read_csv('bug_predictor_sample_dataset.csv')

    # Add columns to put encoded date into
    bug_predictor_sample_dataset['day_of_year'] = 0
    bug_predictor_sample_dataset['week_of_year'] = 0
    bug_predictor_sample_dataset['day_of_week'] = 0
    bug_predictor_sample_dataset['quarter'] = 0
    bug_predictor_sample_dataset['week'] = 0

    # Change the date_merged datatype
    bug_predictor_sample_dataset['date_merged'] = pd.to_datetime(bug_predictor_sample_dataset['date_merged'])

    # Populate encoded date
    for index, row in bug_predictor_sample_dataset.iterrows():
        bug_predictor_sample_dataset.at[index, 'day_of_year'] = row['date_merged'].dayofyear
        bug_predictor_sample_dataset.at[index, 'week_of_year'] = row['date_merged'].weekofyear
        bug_predictor_sample_dataset.at[index, 'day_of_week'] = row['date_merged'].dayofweek
        bug_predictor_sample_dataset.at[index, 'quarter'] = row['date_merged'].quarter
        bug_predictor_sample_dataset.at[index, 'week'] = row['date_merged'].week

    # Set up the requesting_user as a category so that we can encode
    bug_predictor_sample_dataset["requesting_user"] = bug_predictor_sample_dataset["requesting_user"].astype('category')
    bug_predictor_sample_dataset["requesting_user_cat"] = bug_predictor_sample_dataset["requesting_user"].cat.codes

    # Populate training set and target
    X = bug_predictor_sample_dataset[['no_of_commits', 'no_of_files', 'lines_of_code', 'day_of_year', 'week_of_year', 'day_of_week', 'quarter', 'week', 'requesting_user_cat']].copy()
    y = bug_predictor_sample_dataset[['bug_raised_in_uat']].copy()

    # Train/test/split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Build the model
    lm = DecisionTreeClassifier() 
    model = lm.fit(X_train, y_train)

# If this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
    print(("* Loading SKLearn model and Flask starting server..."
        "please wait until server has fully started"))
    train_model()
    Debug(app)
    app.run(debug=True)
    #app.run(host='0.0.0.0')