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
