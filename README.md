# pgtune
An utility to help you tune your postgres config and tables for better performance.

Requirement:
pg_stat_statements. How to install: https://www.postgresql.org/docs/9.4/pgstatstatements.html

INSTALL:
1. Clone the repo.
2. cd /path/pgtune/ pip install -e . 

RUN:
Change the config.py db settings like host, port etc for your db

cmd: pgtune

It will generate a /tmp/pgtune.txt file with tuning logs. 

Limitations/Enhancements needed:
1. Support for parent/child paritioned tables. 
2. Support for composite indexes. 
3. Understanding size of table, and query size to suggest better partitioning. 
4. Understanding no. of orderby and various other sorts to improve on work_mem suggestions.
5. Better understanding of queries to suggest CTEs and Views. 

