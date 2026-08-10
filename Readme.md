# Node.js App with PostgreSQL & Redis in Docker

This repository contains a Node.js application that uses PostgreSQL and Redis, and is Dockerized for easy deployment.


## Prerequisites

Before running the application, make sure you have Docker installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Getting Started

Follow these steps to run the Node.js application with PostgreSQL and Redis in Docker:

1. Clone this repository:

   ```bash
   git clone https://github.com/anasdev0ps/k8s-revision.git nodejs-docker
   ```
2. Navigate to the repository:
    ```bash
   cd nodejs-docker
   ```
3. make a `.env` file following the format of `.env.example` file and set the values
4. build docker images & run containers
    ```bash
   docker-compose up --build
   ```
5. view running containers
    ```bash
   docker ps
   ```

#### You can stop the running containers anytime using this command
```bash
   docker-compose down 
   ```
   

## API Endpoints

### 1. Hello world

- Method: `GET`
- URL: `localhost:3000`
- Description: Just shows hello world
- Response status: `200 OK`
- Response Payload:
  ```
  Hello World!
  ```

### 2. Create user

- Method: `POST`
- URL: `localhost:3000/users`
- Description: Creates a new user
- Request Payload:
  ```json
  {
    "name": "Anas",
    "age": 25
  }
  ```
- Response status: `200 OK`
- Response Payload:
  ```json
  {
    "id": 1,
    "name": "Anas",
    "age": 25,
    "updatedAt": "2024-04-25T16:24:26.490Z",
    "createdAt": "2024-04-25T16:24:26.490Z"
  }
  ```

### 3. Get user list

- Method: `GET`
- URL: `localhost:3000/users`
- Description: Gets list of saved users
- Response status: `200 OK`
- Response Payload:
  ```json
  [
    {
        "id": 1,
        "name": "Anas",
        "age": 25,
        "createdAt": "2024-04-20T18:57:54.001Z",
        "updatedAt": "2024-04-20T18:57:54.001Z"
    },
    {
        "id": 2,
        "name": "Imtiaz",
        "age": 30,
        "createdAt": "2024-04-20T18:58:08.331Z",
        "updatedAt": "2024-04-20T18:58:08.331Z"
    }
  ]
  ```



