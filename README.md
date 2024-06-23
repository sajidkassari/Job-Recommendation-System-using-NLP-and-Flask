# Job Recommendation System

## Overview

The Job Recommendation System is a web application designed to help job seekers find relevant job listings based on their resume content. This project leverages natural language processing (NLP) and machine learning techniques to recommend jobs that best match the skills and experience outlined in the user's resume. The system also includes features for job search, user authentication (signup and login) (still working), and a responsive design for a seamless user experience.

## Features

- **Resume Upload**: Supports uploading resumes in TXT, PDF, DOC, and DOCX formats. Extracts and processes text from the resumes.
- **Job Recommendations**: Uses TF-IDF vectorization and cosine similarity to recommend jobs based on the content of the uploaded resume.
- **Job Search**: Allows users to search for jobs by skills, job titles, or roles.
- **User Authentication**: Includes user signup and login functionality to manage profiles and view personalized job recommendations. (not yet finished)
- **Responsive Design**: Ensures usability across different devices with a user-friendly interface designed using Tailwind CSS.

## Demo

Live website: [Job Recommendation System](https://sajidkassari.pythonanywhere.com/)


## About the Database
- The Database is converted from a dataset of approx 30,000 values which is taken from kaggle (https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset).
- But there is a file called unique_db which only consists of jobs with unique description. Because during the recommendation all the similar jobs had same description and that jobs were only fetched.
- Therefore I created a unique database which narrowed the values from 30,000 to 371.

## Installation

### Prerequisites

- Python 3
- Flask
- SQLite


## Usage
- Access the application at http://localhost:5000.
- Upload a resume to get job recommendations.
- Use the search functionality to find jobs based on specific criteria.
- Sign up and log in to manage your profile.(still remaining)
- 
## File Structure
- **app.py**: Main Flask application file.
- **templates/**: HTML templates for rendering the web pages.
- **static/**: Static files (CSS, JavaScript).
- **unique_database.db**: SQLite database file.
- **requirements.txt**: List of Python dependencies.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request to contribute to the project.
