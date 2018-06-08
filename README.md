# LOGS ANALYSIS
## Project Description
The logs analysis project is part of the Full Stack Nanodegree program by Udacity. This project sets up a mock PostgreSQL database for a fictional news website. The provided Python script uses the psycopg2 library to query the database and produce a report that answers the following three questions:

- What are the most popular three articles of all time
- Who are the most popular article authors of all time
- On which days did more than 1% of requests to the news website lead to errors

## Setup the Environment
The environment used for this project is a virtual machine setup using Vagrant, Virtual Box and some configuration files. You don't have to use the exact same environment to run the project. But if you want to do this, here are the steps you'd take to setup the environment. 

- Use a terminal. If you're on Linux or Mac, your terminal is okay, if you're on Windows, use the Git Bash terminal which you can download here: https://git-scm.com/downloads
- Download and install virtual box from here: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1. 
- Download and install vagrant from here: https://www.vagrantup.com/downloads.html
- Open up your terminal, navigate to the directory you want to use the files in.
- Use vagrant to install bento/ubuntu-16.04 in that directory.

## Getting Started
To run the project and create the output follow these steps: 

1.) Regardless of the environment you choose to use, use a terminal window. In Windows, use the terminal provided by Git Bash.

2.) Download and install PostgreSQL

3.) Download and install Python 2.7 with pip added to the path. 

4.) Install Psycopg2. Learn more about this here http://initd.org/psycopg/docs/install.html
 
 5.) Download newsdata.sql from this link:
 [https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
 
 6.) Setup the database and views

- Use the PostgreSQL psql command line program to create a database named news
- Use the psql command line program to run the SQL statements in newsdata.sql 
- The views I used in this project are available in the create_views.sql file. You can set this up in the command line using 
`psql -d news -f create_views.sql`

7.) Download and install prettytable (this is required for the output formatting used in the program). Install by running the following in the terminal or console window

	pip install prettytable

9.) Run the provided python script in the terminal with the following command

	python newsquestions.py

## VIEWS USED IN THIS PROJECT

The following views were created based on the news database in postgresql

**article_views**
```
    create view article_views as
    select author, title, count(title) as views
    from articles join  log
    on  log.path  =  concat('/article/', articles.slug)
    group by title, author
    order by views desc;
```
**log_status_date**
```
    create view log_status_date as
    select  date::timestamp::date, status
    from (select  time  as  date, status  from  log) as time_log;
```
**log_date_requests**
```
    create view log_date_requests as
    select x.date, total_requests, error_requests, round(error_requests *  100  / total_requests::numeric, 2) as error_percent
    from (select  date, count(status) as total_requests from log_status_date group by  date) as x
    join (select  date, count(status) as error_requests from log_status_date where  status  =  '404 NOT FOUND'  group by  date) as y
    on x.date = y.date;
```
# PROJECT FILES
**newsquestions.py**
This file contains the main code for the logs analysis. It prints the responses to the three questions as output to the console and to a text file.

**create_views.sql**
This file  contains the SQL used to setup the views in the news database.

**newsanalysis.txt**
This file contains sample output from the program.
