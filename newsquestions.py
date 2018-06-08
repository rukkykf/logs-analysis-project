#!/usr/bin/env python2
# Logs analysis project for Udacity Nanodegree by Rukky Kofi

import psycopg2
import datetime
from prettytable import PrettyTable, ALL

db = psycopg2.connect(database="news")
dbcursor = db.cursor()
analysis = open("newsanalysis.txt", 'w')


def tableOutput(tbhead, tbdata, tbtitle):
    # This function will print out tables with two columns
    tbl = PrettyTable(tbhead)
    tbl.hrules = ALL
    tbl.vrules = ALL

    for clmn1, clmn2 in tbdata:
        tbl.add_row([clmn1, clmn2])

    # output to console
    print "\n" + tbtitle
    print tbl.get_string() + "\n"

    # output to file
    analysis.write("\n\n" + tbtitle + "\n" + tbl.get_string())

# Get popular articles
dbcursor.execute("""select title, views
                 from article_views order by views desc limit 3;""")
popular_articles = dbcursor.fetchall()

title = "These are the three most popular articles on the news site:"
tableOutput(["Articles", "views"], popular_articles, title)

# get popular authors
dbcursor.execute("""select name, sum(views) as author_views
                from article_views join authors
                on article_views.author = authors.id
                group by name
                order by author_views desc;""")
popular_authors = dbcursor.fetchall()

title = "These are the authors and their page views:"
tableOutput(["Author Name", "Total Views"], popular_authors, title)

# get days with more than 1% errors
dbcursor.execute("""select date, error_percent
                from log_date_requests
                where error_percent > 1;""")
big_error_days = dbcursor.fetchall()
lst_big_error_days = []

# format the date and error correctly
for day, error in big_error_days:
    lday = day.strftime("%A, %d %B %Y")
    lerror = str(error) + "%"
    lst_big_error_days.append((lday, lerror))

title = "These are the days that have a percentage request higher than 1%:"
tableOutput(["Day", "Error Percentage"], lst_big_error_days, title)
analysis.close()
db.close()
