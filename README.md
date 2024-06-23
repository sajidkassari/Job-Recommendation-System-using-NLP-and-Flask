Job Recommendation System
Overview
The Job Recommendation System is a web application designed to help job seekers find relevant job listings based on their resume content. This project leverages natural language processing (NLP) and machine learning techniques to recommend jobs that best match the skills and experience outlined in the user's resume. The system also includes features for job search, user authentication (signup and login)(still working), and a responsive design for a seamless user experience.

Features
Resume Upload: Supports uploading resumes in TXT, PDF, DOC, and DOCX formats. Extracts and processes text from the resumes.
Job Recommendations: Uses TF-IDF vectorization and cosine similarity to recommend jobs based on the content of the uploaded resume.
Job Search: Allows users to search for jobs by skills, job titles, or roles.
User Authentication: Includes user signup and login functionality to manage profiles and view personalized job recommendations.(not yet finished)
Responsive Design: Ensures usability across different devices with a user-friendly interface designed using Tailwind CSS.


Demo live website:
https://sajidkassari.pythonanywhere.com/

Installation Prerequisites
Python 3
Flask
SQLite

Algorithms
TF-IDF Vectorization
TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a numerical statistic that is intended to reflect the importance of a word in a document relative to a collection of documents.

Term Frequency (TF): Measures how frequently a term occurs in a document.

TF
(
𝑡
,
𝑑
)
=
Number of times term 
𝑡
 appears in document 
𝑑
Total number of terms in document 
𝑑
TF(t,d)= 
Total number of terms in document d
Number of times term t appears in document d
​
 
Inverse Document Frequency (IDF): Measures how important a term is across the entire document collection.

IDF
(
𝑡
)
=
log
⁡
Total number of documents
Number of documents containing term 
𝑡
IDF(t)=log 
Number of documents containing term t
Total number of documents
​
 
TF-IDF Score: The product of TF and IDF.

TF-IDF
(
𝑡
,
𝑑
)
=
TF
(
𝑡
,
𝑑
)
×
IDF
(
𝑡
)
TF-IDF(t,d)=TF(t,d)×IDF(t)
Cosine Similarity
Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space. It is used to determine how similar two documents are irrespective of their size.

Cosine Similarity
(
𝐴
,
𝐵
)
=
𝐴
⋅
𝐵
∥
𝐴
∥
∥
𝐵
∥
Cosine Similarity(A,B)= 
∥A∥∥B∥
A⋅B
​
 
where 
𝐴
⋅
𝐵
A⋅B is the dot product of vectors 
𝐴
A and 
𝐵
B, and 
∥
𝐴
∥
∥A∥ and 
∥
𝐵
∥
∥B∥ are the magnitudes of vectors 
𝐴
A and 
𝐵
B.

Contributing
Contributions are welcome! Please fork the repository and create a pull request to contribute to the project.
