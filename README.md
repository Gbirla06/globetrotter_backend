# Globetrotter Backend

This is the backend service for the Globetrotter application, which provides APIs for user management and destination-related functionalities.

## Tech Stack

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **MongoDB**: A NoSQL database used to store user and destination data.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Python**: The programming language used for the backend development.

## Project Structure

## Endpoints

### Health Check

- **GET** `/health`
  - Checks the connection status to the MongoDB database.
  - **Response**: `{ "status": "connected", "message": "MongoDB is connected!" }` or `{ "status": "error", "message": "Error message" }`

### User Routes

- **GET** `/user`
  - Returns a welcome message for the User Page.
  - **Response**: `{ "message": "Welcome to User Page" }`

- **POST** `/user/register`
  - Registers a new user.
  - **Parameters**: `username: str`
  - **Response**: A dictionary containing user details and a flag indicating if the user already exists.

### Destination Routes

- **GET** `/destination`
  - Returns a welcome message for the Destination Page.
  - **Response**: `{ "message": "Welcome to Destination Page" }`

- **GET** `/destination/random`
  - Gets a random destination.
  - **Response**: A dictionary containing the destination ID, clues, and options.

- **POST** `/destination`
  - Adds new destinations.
  - **Parameters**: `in_data: List[Destination]`
  - **Response**: A success message if data is inserted successfully or a message indicating that the user is not allowed to insert data.

- **POST** `/destination/submit-guess`
  - Submits a guess for a destination.
  - **Parameters**: `guess_data: GuessRequest`
  - **Response**: A dictionary containing the result of the guess, including fun facts, trivia, and updated user scores.

## How to Run

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your MongoDB database and update the connection details in `app/database.py`.
4. Run the FastAPI application using `uvicorn app.main:app --reload`.

## Environment Variables

- `USER_ALLOW_TO_ADD_DATA`: Flag to allow users to add data (default is `False`).

