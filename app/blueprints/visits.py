from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

visits = Blueprint('visits', __name__)

@visits.route('/visits', methods=['GET', 'POST'])
def visit():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new visit
    if request.method == 'POST':
        player_id = request.form['player_id']
        team_id = request.form['team_id']
        visit_date = request.form['visit_date']
        feedback = request.form['feedback']
        status = request.form['status']

        # Insert the new visit into the database
        cursor.execute(
            'INSERT INTO visits (player_id, team_id, visit_date, feedback, status) VALUES (%s, %s, %s, %s, %s)',
            (player_id, team_id, visit_date, feedback, status)
        )
        db.commit()

        flash('New visit added successfully!', 'success')
        return redirect(url_for('visits.visit'))

    # Handle GET request to display all visits
    cursor.execute('SELECT * FROM visits')
    all_visits = cursor.fetchall()
    return render_template('visits.html', all_visits=all_visits)

@visits.route('/update_visit/<int:visit_id>', methods=['GET', 'POST'])
def update_visit(visit_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the visit's details
        player_id = request.form['player_id']
        team_id = request.form['team_id']
        visit_date = request.form['visit_date']
        feedback = request.form['feedback']
        status = request.form['status']

        cursor.execute(
            'UPDATE visits SET player_id = %s, team_id = %s, visit_date = %s, feedback = %s, status = %s WHERE visit_id = %s',
            (player_id, team_id, visit_date, feedback, status, visit_id)
        )
        db.commit()

        flash('Visit updated successfully!', 'success')
        return redirect(url_for('visits.visit'))

    # GET method: fetch visit's current data for pre-populating the form
    cursor.execute('SELECT * FROM visits WHERE visit_id = %s', (visit_id,))
    current_visit = cursor.fetchone()
    return render_template('update_visit.html', current_visit=current_visit)

@visits.route('/delete_visit/<int:visit_id>', methods=['POST'])
def delete_visit(visit_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the visit
    cursor.execute('DELETE FROM visits WHERE visit_id = %s', (visit_id,))
    db.commit()

    flash('Visit deleted successfully!', 'danger')
    return redirect(url_for('visits.visit'))