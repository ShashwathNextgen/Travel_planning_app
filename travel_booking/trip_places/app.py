from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
import sys
import os
from functools import wraps
import logging
import time
import re

from travel_booking.db.db import Places

# Add the db_module folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))


from db import Places

# Configure logging

app = Flask(__name__, static_url_path='/static')

# Set the secret key
app.secret_key = 'give_any_secret_key'



# Database connection parameters
db_host = "localhost"
db_database = "db_name"
db_user = "user_name"
db_password = "user_password"


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search')
        return redirect(url_for('results', search_term=search_term))
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, port=8080)
