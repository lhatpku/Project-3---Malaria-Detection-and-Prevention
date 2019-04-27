import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
from helper.get_event_by_country import get_child_parent_list

app = Flask(__name__)

################## Routes ######################
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sunburst")
def sunburst():
    return jsonify(get_child_parent_list())


if __name__ == "__main__":
    app.run()