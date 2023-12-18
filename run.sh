

# Display a message indicating the start of the server
echo "Starting the Flask server..."

# Set the Flask app environment variable
export FLASK_APP=App.py

# Set the Flask app to run in development mode (optional, for debugging)
export FLASK_ENV=development

# Start the Flask server
flask run

# Display a message indicating the completion of starting the server
echo "Flask server has been started."
