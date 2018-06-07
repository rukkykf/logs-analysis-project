#!/usr/bin/env python2
# Logs analysis project for Udacity Nanodegree by Rukky Kofi

import psycopg2
import datetime
from prettytable import PrettyTable, ALL

db = psycopg2.connect(database="news")
dbcursor = db.cursor()
analysis = open("newsanalysis.txt", 'w')

# Get popular articles
dbcursor.execute("""select title, views
                 from article_views order by views desc limit 3;""")
popular_articles = dbcursor.fetchall()

# print popular articles to console
articlestbl = PrettyTable(['Article Title', 'Views'])
articlestbl.hrules = ALL
articlestbl.vrules = ALL

for article in popular_articles:
    articlestbl.add_row([article[0], article[1]])

print "\nThese are the three most popular articles on the news site:"
print articlestbl
print "\n"

# print popular articles to file
analysis.write("""\nThese are the three most popular
articles on the news site:\n""")

analysis.write(articlestbl.get_string())

# get popular authors
dbcursor.execute("""select name, sum(views) as author_views
                from article_views join authors
                on article_views.author = authors.id
                group by name
                order by author_views desc;""")
popular_authors = dbcursor.fetchall()

# print popular authors to console
authorstbl = PrettyTable(['Author Name', 'Total Views'])
authorstbl.hrules = ALL
authorstbl.vrules = ALL
for author in popular_authors:
    authorstbl.add_row([author[0], author[1]])

print "\nThese are the authors and their page views:"
print authorstbl
print "\n"
analysis.write("""\n\nThese are the authors
and their page views:\n""" + authorstbl.get_string())

# get days with more than 1% errors
dbcursor.execute("""select date, error_percent
                from log_date_requests
                where error_percent > 1;""")
big_error_days = dbcursor.fetchall()

# print the days with more than 1% errors
daystbl = PrettyTable(['Day', 'Percentage of Error Requests'])
for day in big_error_days:
    daystbl.add_row([day[0].strftime("%A, %d %B %Y"), str(day[1]) + "%"])

print "\nThese are the days that have a percentage request higher than 1%:"
print daystbl
print "\n"
analysis.write("""\n\nThese are the days that have a
percentage request higher than 1%:\n""" + daystbl.get_string())
analysis.close()
db.close()
