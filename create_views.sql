create view article_views as
select author, title, count(title) as views
from articles join log
on log.path = concat('/article/', articles.slug)
group by title, author
order by views desc;

create view log_status_date as
select date::timestamp::date, status
from (select time as date, status from log) as time_log;

create view log_date_requests as
select x.date, total_requests, error_requests, round(error_requests * 100 / total_requests::numeric, 2) as error_percent
from (select date, count(status) as total_requests from log_status_date group by date) as x
join (select date, count(status) as error_requests from log_status_date where status = '404 NOT FOUND' group by date) as y
on x.date = y.date;
