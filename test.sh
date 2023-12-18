# !/bin/sh

# Exit immediately if Newman complains
set -e

# Kill the server on exit
trap 'kill $PID' EXIT

# Start the server in the background and record the PID
./run.sh &
PID=$!

# Run Newman with the specified Postman collections and environment
echo "running tests..."
newman run ./forum_multiple_posts.postman_collection.json -e ./env.json # Use the environment file
newman run ./forum_post_read_delete.postman_collection.json -n 50 # 50 iterations
newman run ./forum_get_user_meta_data.postman_collection.json
newman run ./forum_edit_usermetadata.postman_collection.json
newman run ./forum_get_user_meta_data.postman_collection.json
newman run ./forum_search_post_by_user_ext_4_5.postman_collection.json

echo "tests completed"
