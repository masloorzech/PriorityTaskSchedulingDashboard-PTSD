![vite (1)](https://github.com/user-attachments/assets/f1f0a4aa-9037-44d4-ad50-8c1ed6ac2aeb)
# Priority Task Scheduling Dashboard

The **Priority Task Scheduling Dashboard (PTSD)** is an application that helps you create and manage task lists. It offers both a web interface and a terminal interface for managing tasks. The app operates within a Docker environment and stores data in MongoDB for scalability and performance.

## Features

- **Two Interfaces:** 
  - Web Interface (React + Vite)
  - Terminal Interface (Python CLI)
- **Task Creation:** Users can add tasks to their task list.
- **Task Management:** View tasks in a list format, with the ability to mark them as completed.
- **Account Creation:** Allows users to create an account to manage their tasks.
- **Dockerized Deployment:** Easily deployable using Docker Compose.
  
## Requirements

- Docker
- Docker Compose
- MongoDB (used as the database)

## Installation

Follow the instructions below to set up the project locally using Docker.

1. Clone the Repository
2. Build and Run the Application
  Make sure you have Docker and Docker Compose installed.
```bash
docker-compose up --build
```

## Data Storage
The tasks and user data are stored in MongoDB, which is running in a Docker container as part of the application. The schema is flexible, allowing users to have multiple task lists, with each list containing multiple tasks.

## Limitations
- No Task Editing/Deleting in the UI: Users cannot edit or delete tasks through the web interface, but tasks can be deleted via the terminal interface.
- No Sorting/Filtering of Tasks: Tasks are displayed in a simple list format without any filtering or sorting options.

Screenshots
Web Interface

CLI Interface

License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors
Author: Antoni Iwan

Acknowledgements
Docker and Docker Compose for containerization.

MongoDB for scalable, NoSQL database storage.

Flask for the backend API.

React + Vite for the web interface.

Python for the CLI application.


Feel free to modify this template based on your actual project details and adjust things like paths, features, and API endpoints!
