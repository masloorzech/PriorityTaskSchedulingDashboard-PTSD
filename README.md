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

## Screenshots

### Web client
<p align="center">
  <img src="https://github.com/user-attachments/assets/732f8f99-7c26-4d7b-b1dd-375a058994ed" width="45%">
  <img src="https://github.com/user-attachments/assets/1ec9f9bb-38a4-49e7-9248-6f311e83a52f" width="45%">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/aedc4b84-01e2-4f19-b731-e816d01eec70" width="45%">
  <img src="https://github.com/user-attachments/assets/5d53b662-548d-40d8-b280-492050138e93" width="45%">
</p>

### Python CLI
<p align="center">
  <img src="https://github.com/user-attachments/assets/bd438df1-e61d-470e-8a88-4a6273bbbe8a" width="45%">
  <img src="https://github.com/user-attachments/assets/6507678d-ba8d-47b6-abc2-7acb6d097f40" width="45%">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3f199916-28e0-427e-bda0-edc9ba29a037" width="45%">
  <img src="https://github.com/user-attachments/assets/9feec277-3c51-430d-8d16-845050ece55e" width="45%">
</p>

## License
This project is licensed under the MIT License - see the LICENSE file for details.
