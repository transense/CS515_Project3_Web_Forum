#!/bin/bash

# Display a message indicating the start of the test process
echo "Running Postman tests..."

# Start the server using run.sh in the background
./run.sh &

# Capture the PID of the background process
PID=$!

# Wait for the server to start (adjust sleep time if needed)
sleep 5

# Run Postman collections using Newman
newman run forum_multiple_posts.postman_collection.json -e env.json
newman run forum_post_read_delete.postman_collection.json -n 50

# Check the exit code of the Newman runs
if [ $? -eq 0 ]; then
    echo "Postman tests passed successfully."
else
    echo "Postman tests failed."
fi

# Kill the background server process
kill $PID

# Display a message indicating the completion of the test process
echo "Test process completed."
