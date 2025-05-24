# GenAI Career Assistant API

A FastAPI application that provides career assistance for professionals in the Generative AI field.

## Features

- **Learning Resources**: Create tutorials and answer questions about Generative AI
- **Resume Making**: Generate and improve resumes for tech and AI roles
- **Interview Preparation**: Generate interview questions and conduct mock interviews
- **Job Search**: Find job listings based on user criteria

## Setup

1. Clone the repository
2. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ELEVEN_API_KEY=your_eleven_api_key
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```
   or
   ```
   python run.py
   ```

## API Endpoints

### Workflow

- `POST /workflow`: Run the complete workflow based on the user's query

### Learning Resources

- `POST /api/learning/tutorial`: Create a tutorial based on the user's query
- `POST /api/learning/query`: Answer a query about Generative AI

### Interview Preparation

- `POST /api/interview/questions`: Generate interview questions
- `POST /api/interview/mock`: Conduct a mock interview session

### Resume Making

- `POST /api/resume/create`: Create a resume based on user details

### Job Search

- `POST /api/job/search`: Search for jobs based on user criteria

## Documentation

API documentation is available at `/docs` when the server is running.

## Testing

1. Install development dependencies:

   ```
   pip install -r requirements-dev.txt
   ```

2. Run tests:

   ```
   pytest
   ```

3. Generate test coverage report:

   ```
   pytest --cov=app
   ```

4. View the coverage report:
   ```
   open htmlcov/index.html
   ```
