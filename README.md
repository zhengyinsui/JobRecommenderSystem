# Job Recommender System

This project aims at building an easy-used app and strives to help job seekers to get the jobs sooner and help the companies to staff their openings with better-fit candidates, saving time and money for them.

## Important technologies used for this project
Python, Jupyter notebook, Git, Flask, JSON, Pandas, Requests, Heroku, and Bokeh for visualization.

The final product is [a web app](https://jobrecommender.herokuapp.com/). Check it out!

## Setup and deploy
- The main python file is app.py.
- `Procfile`, `requirements.txt`, `conda-requirements.txt`, and `runtime.txt`
  contain some default settings.
- There is some boilerplate HTML in `templates/`

## Background of the project
The job is a very important part of everyone’s life. All of us have experience in searching for jobs. Like now, that’s what we are doing. However, there is inefficiency in the job market. My capstone project is targeting at this problem by providing more information about the job market and building a job recommender system by analyzing a job application dataset from job search website CareerBuilder. There are two parts of the project and the final product will be a web app, which is shown on the screen here.

## Content of the project
None of the job search websites: indeed, Career builder, Glassdoor provide the overview of the job market. On my app, you will be able to look up the overview of the users, job openings or user application habits. For example, this overview figure here shows there are much more job openings available in North Dakoda. It’s less completive to apply for jobs in this state. If you do not care about the working location, you can apply for the jobs in this state. In addition, this figure shows that majority of applicants prefer to apply for jobs from their home state. For example, 95% percent of the users in the texas only apply for jobs from their home states.

The second part of this project is to build a recommender sys. The algorithm I used is item based Collaborative Filtering (CF) algorithm. Here what you need to do is to provide your information. For example, this test user applied for the sales professional job, and the system also recommend this user to apply for sales manager, and retail manager jobs.
