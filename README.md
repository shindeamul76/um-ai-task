<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://github.com/shindeamul76/um-ai-task/">
   <img src="https://superblog.supercdn.cloud/site_cuid_cl4nx9q1v03891pmqfezg0xg9/images/logo-urbanmatch-1687345298740.jpg" alt="Logo">
  </a>

  <h3 align="center">Digital Twin</h3>

  <p align="center">
    Real people - Real places - Real connections.
    <br />
    <a href="https://www.urbanmatch.in/"><strong>Learn more »</strong></a>
    <br />
    <br />
    <a href="https://github.com/shindeamul76/um-ai-task/">Discussions</a>
    ·
    <a href="https://www.infigonfutures.com/">Website</a>
    ·
    <a href="https://github.com/shindeamul76/um-ai-task/issues">Issues</a>
    ·
    <a href="https://www.urbanmatch.in/">Roadmap</a>
  </p>
</p>


## About the Project

# UrbanMatch AI Digital Twin
UrbanMatch is a platform designed to connect real people with real places, fostering genuine connections. Our project utilizes OpenAI's API to create a digital twin that mirrors the real world, enhancing user experiences and interactions.

UrbanMatch leverages cutting-edge technology to provide users with accurate and up-to-date information about various locations and events. By integrating advanced algorithms, data analytics, and OpenAI's powerful models, we ensure that users receive personalized recommendations and insights.

Join us in revolutionizing the way people connect with their surroundings. Explore the endless possibilities with UrbanMatch and be a part of our journey to create meaningful connections.

For more information, visit our [website](https://www.urbanmatch.in/) or check out our [discussions](https://github.com/shindeamul76/um-ai-task/discussions) and [issues](https://github.com/shindeamul76/um-ai-task/issues) on GitHub.


### Built With

- [Django]
- [OpenAI]
- [PostgreSql]
- [SQLAlchemy]
- [Alembic]
- [Redis]

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.10
- PostgreSQL
- Redis
- OpenAI API Key

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/shindeamul76/um-ai-task.git
    ```
2. Copy the .env.example file to .env and add the following variables

3. Create virtual environment
     ```sh
     python -m venv venv
     ```
4. Activate virtual environment
     ```sh
     source venv/bin/activate
     ```
5. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
6. Create a .env file and add the following variables
    ```sh
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/um_ai
    REDIS_URL=redis://localhost:6379/0
    ```
7. Migrate the database
    ```sh
    alembic upgrade head
    ```
8. Run the server
    ```sh
    python manage.py runserver
    ```
9. Add the Questions in the databae
    ```sh    
    python manage.py populate_questions.py



<!-- USAGE EXAMPLES -->
## Usage

To use the application, follow these steps:

1. Sign up for an OpenAI API key at [OpenAI](https://platform.openai.com/signup)
2. Create a .env file and add the following variables
   ```sh
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/um_ai
   REDIS_URL=redis://localhost:6379/0
   DATABASE_URL="postgresql://um-ai-db_owner:BaRHsEA53mVu@ep-black-frog-a1d0y3uc.ap-southeast-1.aws.neon.tech/um-ai-db?sslmode=require"
   DATABASE_NAME=um-ai-db
   DATABASE_USER=
   DTABASE_PASSWORD=
   DATABASE_HOST=
   DATABASE_PORT=5432
   REDIS_HOST= ''
   REDIS_PORT= 17632
   REDIS_PASSWORD= ''
   ```
3. Run the server
   ```sh
   python manage.py runserver   
   ```

## Features
1. I have used the jwt token for authentication focused on the user onboarding process and and giving responses to the user using the open ai api.
2. I have used the redis for caching the user's questionnaire answers.
3. I have also Keeping the cnversion history in the redis to keep track of the conversation history.

# Note: -  Calling the message send and receive api will take some time to respond as it is calling the open ai api and the conversation history is being stored in the redis cache and the questionnaire answers are being cached in the redis so it will take around 4-5 seconds to respond but we can improve this.

# Note: - I have also attached the postman collection for the api calls in the postman folder.

<div align="center">

  <img src="/assests/Flow.png"  width="100%" height="300" alt="Flow">
</div>

# Endpoints

## POST /api/v1/messages/

Send a message and generate a response using GPT.

### Parameters

- `sender_id`: The ID of the sender.
- `recipient_id`: The ID of the recipient.
- `content`: The content of the message.

### Response

- `message_id`: The ID of the message.
- `sender_id`: The ID of the sender.
- `recipient_id`: The ID of the recipient.
- `content`: The content of the message.
- `response`: The response generated by the AI.

### Example

```json
{
  "message_id": 1,
  "sender_id": 1,
  "recipient_id": 2,
  "content": "Hello, how are you?",
  "response": "I'm doing well, thank you for asking. How about you?"
}
```

## GET /api/v1/messages/<user_id>/

Retrieve message history for a user.

### Parameters

- `user_id`: The ID of the user.

### Response

- `messages`: A list of messages.
- `sender_id`: The ID of the sender.
- `recipient_id`: The ID of the recipient.
- `content`: The content of the message.
- `response`: The response generated by the AI.

### Example

```json
[
  {
    "message_id": 1,
    "sender_id": 1,
    "recipient_id": 2,
    "content": "Hello, how are you?",
    "response": "I'm doing well, thank you for asking. How about you?"
  },
  {
    "message_id": 2,
    "sender_id": 2,
    "recipient_id": 1,
    "content": "I'm doing well, thank you for asking. How about you?",
    "response": "I'm doing well, thank you for asking. How about you?"
  }
]
```

## POST /users/create/

Create a new user.

### Parameters

- `name`: The name of the user.
- `phone_number`: The phone number of the user (unique).
- `age`: The age of the user.
- `sex`: The sex of the user.
- `location`: The location of the user.
- `job_title`: The job title of the user.
- `company_name`: The company name of the user.
- `education`: The education level of the user.

### Response

- `user_id`: The ID of the user.
- `name`: The name of the user.
- `phone_number`: The phone number of the user.
- `age`: The age of the user.
- `sex`: The sex of the user.
- `location`: The location of the user.
- `job_title`: The job title of the user.
- `company_name`: The company name of the user.
- `education`: The education level of the user.

### Example

```json
{
    "user_id": 1,
    "name": "John Doe",
    "phone_number": "1234567890",
    "age": 30,
    "sex": "Male",
    "location": "New York",
    "job_title": "Software Engineer",
    "company_name": "Tech Corp",
    "education": "Master's Degree"
}
```
