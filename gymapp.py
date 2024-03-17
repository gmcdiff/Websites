from flask import Flask, request, jsonify, render_template

import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('gymindex.html')

@app.route('/gymexercises.html')
def gym_exercises():
    return render_template('gymexercises.html')

# Endpoint to handle AJAX requests
@app.route('/fetch_exercises', methods=['POST', 'GET'])
def fetch_exercises():
    # Get selected values from the frontend
    type_selected = request.args.get('type')
    area_selected = request.args.get('area')
    level_selected = request.args.get('level')

    # Convert type, area, and level to lowercase
    type_selected = type_selected.lower()
    area_selected = area_selected.lower()
    level_selected = level_selected.lower()

    # Establish connection to SQLite database
    conn = sqlite3.connect('workout.db')
    cursor = conn.cursor()

    # Execute SELECT query based on selected criteria
    cursor.execute("SELECT * FROM Exercises WHERE LOWER(type)=? AND REPLACE(LOWER(area), ' ', '')=? AND LOWER(level)=?", 
                   (type_selected, area_selected, level_selected))
    
    # Fetch rows that match the criteria
    fetched_rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return fetched rows as JSON response
    return jsonify(exercises=fetched_rows)

if __name__ == '__main__':
    app.run(debug=True)