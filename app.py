import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import PyPDF2
import re
import numpy as np
from flask import session, redirect, url_for
import auth


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'doc', 'docx'}
app.secret_key='jrs123'



# Function to check if the filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Placeholder function to extract text from a resume
def extract_text_from_resume(resume_filepath):
    # Check the file extension
    _, file_extension = os.path.splitext(resume_filepath)
    
    # Extract text based on the file extension
    if file_extension.lower() == '.txt':
        with open(resume_filepath, 'r', encoding='utf-8') as file:
            text = file.read()
    elif file_extension.lower() == '.pdf':
        text = ''
        with open(resume_filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()
    elif file_extension.lower() == '.docx':
        text = docx2txt.process(resume_filepath)
    else:
        # Unsupported file format
        text = None
    return text

# Connect to the SQLite database
conn = sqlite3.connect('unique_database.db')

# Read data from the 'jobs' table into a pandas DataFrame
jobs_data = pd.read_sql_query("SELECT * FROM unique_jobs", conn)

# Preprocessing the job descriptions
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Concatenate job text for TF-IDF vectorization
job_text = jobs_data['Job Title'] + ' ' + jobs_data['skills'] + ' ' + jobs_data['Role'] + ' ' + jobs_data['Responsibilities']

# Fit and transform TF-IDF vectors for job text
job_tfidf_matrix = tfidf_vectorizer.fit_transform(job_text)

# Function to identify the type of query (skill, job title, or role)
def identify_query_type(query):
    # Simple classification based on the structure of the query
    if re.search(r'\b(?:skill|skills)\b', query, re.IGNORECASE):
        return 'skill'
    elif re.search(r'\b(?:title)\b', query, re.IGNORECASE):
        return 'job title'
    elif re.search(r'\b(?:role)\b', query, re.IGNORECASE):
        return 'role'
    else:
        # Default to job title if no specific indicator found
        return 'job title'




'''previous algorithm'''
'''
# Function to recommend jobs based on a given resume
def recommend_jobs(resume_text, num_recommendations=5):
    # Calculate TF-IDF vectors for the resume and job descriptions
    resume_vector = tfidf_vectorizer.transform([resume_text])
    job_desc_vectors = tfidf_vectorizer.transform(jobs_data['Job Description'])

    # Calculate cosine similarity based on job descriptions
    cosine_similarities_desc = cosine_similarity(resume_vector, job_desc_vectors).flatten()

    # Calculate TF-IDF vectors for other relevant features
    features_to_consider = ['Experience', 'Job Title', 'Role', 'skills', 'Responsibilities']
    job_feature_vectors = tfidf_vectorizer.transform(jobs_data[features_to_consider].fillna('').apply(lambda x: ' '.join(x), axis=1))

    # Calculate cosine similarity based on other features
    cosine_similarities_features = cosine_similarity(resume_vector, job_feature_vectors).flatten()

    # Combine the similarity scores from both descriptions and other features
    combined_similarities = 0.6 * cosine_similarities_desc + 0.4 * cosine_similarities_features

    # Get indices of top recommended jobs based on combined similarity scores
    top_indices = combined_similarities.argsort()[-num_recommendations:][::-1]

    # Get the recommended job listings
    recommended_jobs = jobs_data.iloc[top_indices]

    # Calculate the matching percentage based on combined similarity scores
    recommended_jobs['Matching_Percentage'] = combined_similarities[top_indices] * 100

    return recommended_jobs

'''






'''new algorithm'''


# Function to recommend jobs based on a given resume
def recommend_jobs(resume_text, num_recommendations=5):
    # Calculate TF-IDF vectors for the resume and job descriptions
    resume_vector = tfidf_vectorizer.transform([resume_text])
    job_desc_vectors = tfidf_vectorizer.transform(jobs_data['Job Description'])
    job_title_vectors = tfidf_vectorizer.transform(jobs_data['Job Title'])
    role_vectors = tfidf_vectorizer.transform(jobs_data['Role'])
    skills_vectors = tfidf_vectorizer.transform(jobs_data['skills'])

    # Calculate cosine similarity based on job descriptions
    cosine_similarities_desc = cosine_similarity(resume_vector, job_desc_vectors).flatten()

    # Calculate cosine similarity based on job title
    cosine_similarities_title = cosine_similarity(resume_vector, job_title_vectors).flatten()

    # Calculate cosine similarity based on roles
    cosine_similarities_roles = cosine_similarity(resume_vector, role_vectors).flatten()

    # Calculate cosine similarity based on skills
    cosine_similarities_skills = cosine_similarity(resume_vector, skills_vectors).flatten()

    # Combine the cosine similarity scores from all components
    combined_similarities = np.vstack((cosine_similarities_desc, cosine_similarities_title, cosine_similarities_roles, cosine_similarities_skills)).max(axis=0)

    # Get indices of top recommended jobs based on combined similarity scores
    top_indices = combined_similarities.argsort()[-num_recommendations:][::-1]

    # Get the recommended job listings
    recommended_jobs = jobs_data.iloc[top_indices]

    # Calculate the matching percentage based on combined similarity scores
    matching_percentages = combined_similarities[top_indices] * 100
    matching_percentages = [round(percentage, 2) for percentage in matching_percentages]
    recommended_jobs['Matching_Percentage'] = matching_percentages

    return recommended_jobs




######################################

def get_random_jobs(num_jobs=12):
    # SQL query to fetch random jobs from the database
    conn = sqlite3.connect('unique_database.db')
    cursor = conn.cursor()
    sql_query = "SELECT * FROM unique_jobs ORDER BY RANDOM() LIMIT ?"
    cursor.execute(sql_query, (num_jobs,))
    random_jobs = cursor.fetchall()

    # Convert the fetched jobs into a list of dictionaries
    jobs_data = []
    for job in random_jobs:
        job_dict = {
            "company": job[21],
            "title": job[14],
            "location": job[5],
            "salary_range": job[3],
            "worktype": job[8]
        }
        jobs_data.append(job_dict)

    return jobs_data

@app.route('/')
def index():
    # Fetch 12 random jobs initially
    random_jobs = get_random_jobs()
    num_columns = 4
    grouped_jobs = [random_jobs[i:i+num_columns] for i in range(0, len(random_jobs), num_columns)]
    return render_template('index.html', grouped_jobs=grouped_jobs)

@app.route('/refresh_jobs', methods=['POST'])
def refresh_jobs():
    # Fetch 12 new random jobs when the refresh button is clicked
    random_jobs = get_random_jobs(300)
    num_columns = 4
    grouped_jobs = [random_jobs[i:i+num_columns] for i in range(0, len(random_jobs), num_columns)]
    return render_template('alljobs.html', grouped_jobs=grouped_jobs)

#################################################################

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resume_text = extract_text_from_resume(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Placeholder function
        recommended_jobs = recommend_jobs(resume_text)
        return render_template('job_listings.html', job_listings=recommended_jobs.to_dict(orient='records'))
    return redirect(request.url)


@app.route('/search', methods=['GET', 'POST'])
def search_jobs():
    query = request.args.get('query')
    if query:
        print("Received search query:", query)  # Debug statement
        
        # Identify the type of query (skill, job title, or role)
        query_type = identify_query_type(query)
        print("Identified query type:", query_type)  # Debug statement

        # Transform the query into a TF-IDF vector
        query_vector = tfidf_vectorizer.transform([query])

        # Calculate cosine similarity between the query vector and job TF-IDF matrix
        cosine_similarities = cosine_similarity(query_vector, job_tfidf_matrix).flatten()

        # Get indices of jobs with high similarity
        top_indices = cosine_similarities.argsort()[::-1]

        # Filter jobs based on cosine similarity threshold
        threshold = 0.2  # Adjust as needed
        filtered_jobs = jobs_data.iloc[top_indices][cosine_similarities[top_indices] > threshold]

        print("Number of filtered jobs:", len(filtered_jobs))  # Debug statement

        # Calculate matching percentage and add it to the DataFrame
        matching_percentages = cosine_similarities[top_indices][cosine_similarities[top_indices] > threshold] * 100
        matching_percentages = [round(percentage, 2) for percentage in matching_percentages]
        filtered_jobs['Matching_Percentage'] = matching_percentages

        # Render the job listings template with filtered jobs
        return render_template('search_result.html', job_listings=filtered_jobs.to_dict(orient='records'), query=query, query_type=query_type)
    else:
        # If no query provided, render an empty job listings page
        return render_template('search_result.html', job_listings=[], query='', query_type='')





@app.route('/job_listings')
def job_listings():
    if not auth.user_logged_in():
        return redirect(url_for('login'))
    return render_template('job_listings.html')

@app.route('/search_result')
def search_result():
    if not auth.user_logged_in():
        return redirect(url_for('login'))
    return render_template('search_result.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check login credentials
        username = request.form['username']
        password = request.form['password']
        # Logic to authenticate user
        if auth.authenticate_user(username, password):
            session['user_id'] = auth.get_user_id(username)
            return redirect(url_for('index'))  # Redirect to homepage after successful login
        else:
            return('Invalid username or password', 'error')
    # Render login page
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Check if username already exists
        if auth.user_exists(username):
            return('Username already exists', 'error')
        # Check if passwords match
        elif password != confirm_password:
            return('Passwords do not match', 'error')
        else:
            # Add user to the database
            auth.add_user(username, password)
            return('User created successfully. Please login.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful signup
    # Render signup page
    return render_template('signup.html')





if __name__ == '__main__':
    app.run(debug=True)
