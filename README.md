The logs analysis project makes use of the Python db-api using psycopg2 and postresql to obtain analysis data from the news database provided by Udacity as part of the logs analysis project in the Full Stack Developer nanodegree. The program outputs its results to a text file called newsanalysis.txt, as well as to the terminal window. 

# GETTING STARTED
To run the project and create the webpage follow these steps: 

1.) Download and install Python 2.7, you can get that here 
    https://www.python.org/download/releases/2.7/
   
2.) Download and install prettytable (this is required for the output formatting used in the program). Install by running the following in the terminal or console window

	pip install prettytable

3.) Setup and install psycopg2. Get more information here
     http://initd.org/psycopg/docs/install.html
     
4.) Run the project in the terminal with the following command

	python newsquestions.py

# VIEWS USED IN THIS PROJECT

The following views were created based on the news database in postgresql

**article_views**
create view article_views as
select author, title, count(title) as views
from articles join log
on log.path = concat('/articles/', articles.slug)
group by title, author
order by views desc;

**log_status_date**
create view log_status_date
select date::timestamp::date, status
from (select time at time zone 'UTC-1' as date, status from log) as one_time_zone;

**log_date_requests**
create view log_date_requests as
select x.date, total_requests, error_requests, round(error_requests * 100 / total_requests::numeric, 2) as error_percent
from (select date, count(status) as total_requests from log_status_date group by date) as x
join (select date, count(status) as error_requests from log_status_date where status = '404 NOT FOUND' group by date) as y
on x.date = y.date;

# PROJECT FILES
**newsquestions.py**
This file contains the main code for the logs analysis. The SQL statements and the responses to the three questions 

**newsanalysis.txt**
This file contains sample output from the program.