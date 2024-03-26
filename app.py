from flask import Flask, request, jsonify, render_template
from itertools import product
import sqlite3

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('musicindex.html')

@app.route('/templates/musicindex.html')
def music_index():
    return render_template('musicindex.html')

@app.route('/templates/recipesindex.html')
def recipes_index():
    return render_template('recipesindex.html')

@app.route('/templates/tripindex.html')
def trip_index():
    return render_template('tripindex.html')

@app.route('/templates/romeindex.html')
def rome_index():
    return render_template('romeindex.html')

@app.route('/templates/switzerlandindex.html')
def switzerland_index():
    return render_template('switzerlandindex.html')

@app.route('/templates/gymindex.html')
def gym_index():
    return render_template('gymindex.html')

@app.route('/templates/gymexercises.html')
def gym_exercises():
    return render_template('gymexercises.html')

# Endpoint to handle AJAX requests
@app.route('/fetch_exercises', methods=['POST', 'GET'])
def fetch_exercises():
    # Get selected values from the frontend
    equip_selected = request.args.getlist('equipment')
    area_selected = request.args.getlist('area')
    print(equip_selected)
    print(area_selected)
    # Split comma-separated values within each element
    equip_selected = [equip.split(',') for equip in equip_selected]
    area_selected = [area.split(',') for area in area_selected]
    print(equip_selected)
    print(area_selected)
    # Flatten the list of lists
    equip_selected = [item for sublist in equip_selected for item in sublist]
    area_selected = [item for sublist in area_selected for item in sublist]
    print(equip_selected)
    print(area_selected)
    # Establish connection to SQLite database
    conn = sqlite3.connect('workout.db')
    cursor = conn.cursor()

    # Create an empty list to store combinations
    combinations = []

    # Create combinations of equipment and area
    combinations = list(product(equip_selected, area_selected))
    print(combinations)
    # Construct placeholders for parameters in the query
    placeholders = ' OR '.join(['(Equipment = ? AND Bodypart = ?)'] * len(combinations))
    print(placeholders)
    # Construct the query
    query = f"""
    SELECT *
    FROM Exercises
    WHERE {placeholders}
    """
    print(query)
    # Execute the query with parameters
    cursor.execute(query, [item for sublist in combinations for item in sublist])

    # Fetch rows that match the criteria
    fetched_rows = cursor.fetchall()
    print(fetched_rows)
    # Close the database connection
    conn.close()

    # Return fetched rows as JSON response
    return jsonify(exercises=fetched_rows)

if __name__ == '__main__':
    app.run(debug=True)