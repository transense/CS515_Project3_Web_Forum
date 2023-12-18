#  name and Stevens login

1) Nikunj Arvindbhai Gothadiya ngothadi@stevens.edu
2) Vaibhavi Nikeshkumar Shah vshah6@stevens.edu

# the URL of your public GitHub repo

https://github.com/transense/CS515_Project3_Web_Forum

# an estimate of how many hours you spent on the project

We spent around 95 hours on the project.

# a description of how you tested your code

We employed a comprehensive testing strategy to ensure the robustness and reliability of the Flask web application. The testing process encompassed unit testing, integration testing, concurrency testing, user acceptance testing (UAT), error handling scenarios, regression testing, and documentation.

Unit Testing: We utilized the unittest module in Python to conduct unit testing for critical functions within the application. For instance, functions like create_post, read_post, and delete_post were subjected to a better of test cases. These included valid inputs, edge cases, and error conditions such as malformed JSON requests.

Integration Testing: Integration testing focused on validating the seamless interaction between different components. We tested the integration of Flask routes, data storage, and user authentication mechanisms. Mock data was employed to simulate interactions with external APIs or databases.

Concurrency and Thread Safety Testing: Given the threading aspect of the application, We designed and executed tests to evaluate thread safety. Scenarios were created to simulate concurrent access to shared resources, especially the posts dictionary. This ensured that locks were effective in preventing data corruption and race conditions.

User Acceptance Testing (UAT): User acceptance testing involved sharing a version of the application with team members and stakeholders. Their feedback was solicited to assess the user interface, functionality, and overall user experience. This feedback loop helped validate that the application met the intended requirements.

Error Handling and Edge Cases: A systematic approach was taken to test error handling and edge cases. Invalid input scenarios, such as malformed JSON requests and missing parameters, were systematically tested. Additionally, edge cases, such as handling an empty posts dictionary or an invalid date format, were thoroughly addressed.

Regression Testing: After each code modification, regression testing was conducted. This involved rerunning existing test cases to ensure that new changes did not introduce regressions. Exploratory testing was also performed to identify any unexpected side effects.

Documentation and Code Review: Test cases were documented in a separate test suite, and comments were included within the code to explain critical sections. The code underwent peer review, during which team members provided feedback on code structure, clarity, and adherence to best practices.

This testing approach aimed to ensure the application's stability, functionality, and adherence to both functional and non-functional requirements.


# any bugs or issues you could not resolve

No bugs and issues 


# an example of a difficult issue or bug and how you resolved

create posts: One challenging issue I encountered was a deadlock scenario during concurrent post creation in the application. Users attempting to create posts simultaneously caused the system to become unresponsive due to the contention for locks on shared resources. To resolve this, I conducted a thorough analysis of the code, focusing on the sections related to post creation and lock usage. I refined the granularity of locks, shifting from a global lock for the entire posts dictionary to more fine-grained locks on specific posts. Additionally, I ensured a consistent order of lock acquisition to prevent circular waiting, a common cause of deadlocks. Rigorous testing, including simulated concurrent post creation scenarios, was crucial to identifying and rectifying potential issues. I introduced logging and monitoring to track lock acquisitions and releases, enabling me to analyze the flow of locks during different operations. Load testing under high concurrency was performed to validate the solution's effectiveness. Collaboration with team members through peer review further confirmed the correctness of the changes. Ultimately, these measures successfully eliminated the deadlock issue, enhancing the application's resilience to concurrent operations and improving overall stability and performance.

Session Management: A challenging issue emerged in the application regarding session management and user authentication, manifesting as inconsistent session states leading to unauthorized access and unexpected logouts for users. In response, a meticulous review of the authentication flow was initiated, focusing on login, logout, and session creation processes. The session token generation was revisited to ensure uniqueness and robust security practices. Adjustments to session expiration policies were made to mitigate unexpected logouts, incorporating appropriate timeouts and reauthentication prompts. Given the concurrent nature of web applications, measures were implemented to handle simultaneous access to user sessions, employing locks or atomic operations to prevent race conditions. An audit trail and extensive logging were introduced to aid in diagnosing session-related issues, tracking authentication events, and expirations. User testing validated the changes under real-world scenarios, including concurrent logins and logouts. A final layer of security review ensured that the adjustments did not introduce vulnerabilities. The outcome was a successful resolution of the session management and authentication issues, resulting in improved consistency, enhanced security, and a more reliable user experience.


# a list of the five extensions you’ve chosen to implement; be sure to describe the endpoints you’ve added to support this, using a documentation format similar to ours

1) Users and user keys
2) User profiles (needs user)
3) Threaded replies
4) Date- and time-based range queries
5) User-based range queries (needs user)

Extension 1: Users and User Keys
    Endpoint: GET /users
    
    Description: Retrieve a list of all users along with their basic information.
    Response:
    
            [
              {
                "user_id": 1,
                "username": "Nik_Gothadiya",
                "email": "nik@gothadiya.com"
              },
              {
                "user_id": 2,
                "username": "v_shah",
                "email": "v@shah.com"
              }
            ]
    Endpoint: POST /user/register
    
    Description: Register a new user and generate a unique user key.
    Request Body:
    
            {
              "username": "new_user",
              "email": "new@123.com"
            }
    Response:
    
            {
              "user_id": 3,
              "username": "new_user",
              "email": "new@123.com",
              "user_key": "unique_user_key"
            }

Extension 2: User Profiles (Needs User)
    Endpoint: GET /user/{user_id}/profile
    Description: Retrieve the detailed profile information for a specific user.
    Parameters:
    {user_id} (int): The unique identifier of the user.
    Response:
            {
              "user_id": 1,
              "username": "nik_gothadiya",
              "email": "nik@gothadiya.com",
              "full_name": "nik gothadiya",
              "join_date": "2023-01-01T12:00:00",
              "post_count": 42
            }
            
Extension 3: Threaded Replies
    Endpoint: POST /api/posts/{postId}/replies
    Description: Create a new threaded reply for a specific post.
    Request Body:
    {
      "text": "The content of the threaded reply",
      "parentReplyId": "optional parent reply ID, null if top-level reply"
    }
    Response:
    201 Created - Successfully created the threaded reply.
    400 Bad Request - Invalid request body.
    404 Not Found - Post not found.
    
    2. Get Threaded Replies for a Post
    Endpoint: GET /api/posts/{postId}/replies
    Description: Retrieve all threaded replies for a specific post.
    Response:
    json
    Copy code
    [
      {
        "id": "replyId",
        "text": "The content of the threaded reply",
        "createdAt": "timestamp",
        "user": {
          "id": "userId",
          "username": "username"
        },
        "replies": [
          {
            "id": "nestedReplyId",
            "text": "The content of the nested reply",
            "createdAt": "timestamp",
            "user": {
              "id": "userId",
              "username": "username"
            }
          },
          // ... more nested replies
        ]
      },
      // ... more top-level replies
    ]
    Response Codes:
    200 OK - Successfully retrieved threaded replies.
    404 Not Found - Post not found.
    
    3. Get Single Threaded Reply
    
    Endpoint: GET /api/posts/{postId}/replies/{replyId}
    Description: Retrieve a single threaded reply.
    Response:
    {
      "id": "replyId",
      "text": "The content of the threaded reply",
      "createdAt": "timestamp",
      "user": {
        "id": "userId",
        "username": "username"
      },
      "replies": [
        {
          "id": "nestedReplyId",
          "text": "The content of the nested reply",
          "createdAt": "timestamp",
          "user": {
            "id": "userId",
            "username": "username"
          }
        },
        // ... more nested replies
      ]
    }
    Response Codes:
    200 OK - Successfully retrieved the threaded reply.
    404 Not Found - Reply or post not found.
    
Extension 4: Date- and Time-Based Range Queries
    Endpoint: GET /posts/date-range
    Description: Retrieve posts within a specified date and time range.
    Query Parameters:
    start_date (string, ISO 8601 format): The start date for the range.
    end_date (string, ISO 8601 format): The end date for the range.
    Response:
            [
              {
                "id": 1,
                "timestamp": "2023-02-15T14:30:00",
                "msg": "Post within date range"
              },
              {
                "id": 2,
                "timestamp": "2023-02-20T09:45:00",
                "msg": "Another post within date range"
              }
            ]

Extension 5: User-Based Range Queries (Needs User)
    Endpoint: GET /user/{user_id}/posts
    Description: Retrieve posts created by a specific user within a specified date and time range.
    Parameters:
    {user_id} (int): The unique identifier of the user.
    Query Parameters:
    start_date (string, ISO 8601 format): The start date for the range.
    end_date (string, ISO 8601 format): The end date for the range.
    Response:
            [
              {
                "id": 1,
                "timestamp": "2023-02-15T14:30:00",
                "msg": "User-specific post within date range"
              },
              {
                "id": 2,
                "timestamp": "2023-02-20T09:45:00",
                "msg": "Another user-specific post within date range"
              }
            ]
            
Extension 5: Sessions (Needs Users)
    Endpoint: POST /user/{user_id}/login
    Description: Log in a user and create a session.
    Parameters:
    {user_id} (int): The unique identifier of the user.
    Response:
            {
              "user_id": 1,
              "session_token": "unique_session_token",
              "expiration_time": "2023-03-01T18:00:00"
            }
    Endpoint: POST /user/{user_id}/logout
    Description: Log out a user and invalidate the session.
    Parameters:
    {user_id} (int): The unique identifier of the user.
    Response:
        {
          "user_id": 1,
          "message": "User successfully logged out"
        }
These extensions add functionality related to users, user profiles, date- and time-based range queries, user-based range queries, and sessions to the existing API. Adjust the details based on your specific application requirements and design.


# detailed summaries of your tests for each of your extensions, i.e., how to interpret your testing framework and the tests you’ve written

Extension 1: Users and User Keys
    
    Testing Framework:
    
    Test Suite: Implemented using the unittest framework in Python.
    Mock Data: Utilized mock data for user registration and retrieval scenarios.
    Tests:
    
    Test User Registration:
    Description: Verifies that a new user can successfully register.
    Steps:
    Send a POST request to /user/register with mock user data.
    Check if the response includes the expected user details and a unique user key.
    Test List of Users:
    Description: Verifies the endpoint /users returns a list of all users.
    Steps:
    Send a GET request to /users.
    Check if the response contains the expected list of users.


Extension 2: User Profiles (Needs User)

    Testing Framework:
    
    Test Suite: Extended the existing unittest suite.
    Mock Data: Created mock user profiles for testing.
    Tests:
    
    Test User Profile Retrieval:
    Description: Verifies that the user profile endpoint /user/{user_id}/profile returns accurate user details.
    Steps:
    Send a GET request to /user/{user_id}/profile.
    Check if the response matches the expected user profile.
    
Extension 3: Threaded Replies

    Testing Framework:

    Test Suite: Utilized a combination of unittest and integration testing frameworks.
    Mock Data: Generated test data with various threaded reply structures for comprehensive testing.
    Tests:

    Test Create Threaded Reply Endpoint:
    Description: Validates the /api/posts/{postId}/replies endpoint for creating threaded replies.
    Steps:
    - Send a POST request to /api/posts/{postId}/replies with valid and invalid payloads.
    - Check for the expected HTTP response codes and verify the creation of threaded replies.

    Test Get Threaded Replies for a Post Endpoint:
    Description: Confirms the /api/posts/{postId}/replies endpoint retrieves threaded replies for a post.
    Steps:
    - Send a GET request to /api/posts/{postId}/replies.
    - Examine the response structure for correctness and check for the presence of threaded replies.

    Test Get Single Threaded Reply Endpoint:
    Description: Validates the /api/posts/{postId}/replies/{replyId} endpoint for retrieving a single threaded reply.
    Steps:
    - Send a GET request to /api/posts/{postId}/replies/{replyId}.
    - Verify the response structure and confirm the retrieval of the specified threaded reply.

    Integration Test Create and Retrieve Threaded Replies:
    Description: End-to-end testing for creating and retrieving threaded replies.
    Steps:
    - Simulate user interactions: create a post, add threaded replies, and retrieve the post with replies.
    - Ensure the retrieved post contains the expected threaded reply structure.

    Integration Test Error Handling:
    Description: Validates error handling scenarios for the Threaded Replies extension.
    Steps:
    - Test creating threaded replies for a non-existent post and verify the 404 Not Found status.
    - Test retrieving threaded replies for a non-existent post and confirm the 404 Not Found status.


Extension 4: Date- and Time-Based Range Queries
    Testing Framework:
    
    Test Suite: Leveraged the unittest framework.
    Mock Data: Generated posts with different timestamps for testing date-range queries.
    Tests:
    
    Test Date-Range Query:
    Description: Verifies that the /posts/date-range endpoint returns posts within the specified date range.
    Steps:
    Send a GET request to /posts/date-range with start_date and end_date parameters.
    Check if the response contains posts within the specified date range.
    
    
Extension 5: User-Based Range Queries (Needs User)
    Testing Framework:
    
    Test Suite: Integrated with the existing unittest suite.
    Mock Data: Extended mock posts with user-specific timestamps.
    Tests:
    
    Test User-Based Date-Range Query:
    Description: Ensures that the /user/{user_id}/posts endpoint returns posts by a user within the specified date range.
    Steps:
    Send a GET request to /user/{user_id}/posts with start_date and end_date parameters.
    Check if the response contains posts by the specified user within the date range.
