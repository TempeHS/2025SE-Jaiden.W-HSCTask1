from flask import redirect, flash, session, send_file, url_for
import io
import json
from databaseManagement import retrieveUserData, deleteUserData

def downloadData(app):
    if 'username' not in session:
        app.logger.warning('Unauthorized access attempt to download data.')
        return redirect(url_for('login'))
    username = session['username']
    app.logger.info(f'Received download data request for user: {username}')
    user_data = retrieveUserData(username)
    if not user_data:
        flash('No data found for the user.', 'danger')
        app.logger.info(f'No data found for user: {username}')
        return redirect(url_for('profile'))
    # Convert user data to JSON
    user_data_json = json.dumps(user_data)
    # Create a BytesIO object and write the JSON data to it
    buffer = io.BytesIO()
    buffer.write(user_data_json.encode('utf-8'))
    buffer.seek(0)
    app.logger.info(f'Data downloaded for user: {username}')
    return send_file(buffer, as_attachment=True, download_name=f"{username}_data.json", mimetype='application/json')

def deleteData(app):
    if 'username' not in session:
        app.logger.warning('Unauthorized access attempt to delete data.')
        return redirect(url_for('login'))
    username = session['username']
    success = deleteUserData(username)
    if success:
        flash('Your data has been deleted successfully.', 'success')
        app.logger.info(f'Data deleted for user: {username}')
        session.clear()  # Clear the session after deleting user data
        return redirect(url_for('sign_up'))
    else:
        flash('An error occurred while deleting your data. Please try again later.', 'danger')
        app.logger.error(f'Error deleting data for user: {username}')
        return redirect(url_for('profile'))