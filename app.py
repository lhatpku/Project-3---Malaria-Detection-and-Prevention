import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, flash, request, redirect, render_template
from sqlalchemy import create_engine
from helper.get_event_by_country import get_child_parent_list, get_incident_by_years
from helper.get_event_by_age_group import get_event_by_age_group
from werkzeug.utils import secure_filename
from ml.Malaria_CNN_Test_Model import predict
from keras.models import load_model
import tensorflow as tf

global graph
graph = tf.get_default_graph()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'static/image'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

default_file = 'C12NThinF_IMG_20150614_124212_cell_138.png'
model_loc = os.path.join('ml','Malaria_CNN_Trained7.h5')

model = load_model(model_loc)

# print(predict(model,os.path.join(app.config['UPLOAD_FOLDER'], default_file)))
################## Routes ######################
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data/sunburst')
def sunburst():
    return jsonify(get_child_parent_list())

@app.route('/data/dist/death')
def dist_death():
    return jsonify(get_incident_by_years())

@app.route('/data/age/death')
def age_death():
    return jsonify(get_event_by_age_group())

@app.route('/data/mosquitoes')
def mosquitoes():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mosquitoes_loc = os.path.join(__location__,'data/trend/mosquitoes2.csv')
    mosquitoes = pd.read_csv(mosquitoes_loc)
    moquitoes_dict = mosquitoes.to_dict(orient='records')
    return(jsonify(moquitoes_dict))


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        try:
            f = request.files['file']

            # Save the file to ./uploads
            basepath = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(
                basepath, app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(file_path)

            # Make prediction
            with graph.as_default():
                preds = predict(model,file_path)

            return preds
        except Exception as e:
            return f'Excpetion: {e}'
    return None


    
if __name__ == "__main__":
    app.run(debug=False)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()

