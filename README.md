# pgtune
An utility to help you tune your postgres config and tables for better performance.

Requirement:
pg_stat_statements. How to install: https://www.postgresql.org/docs/9.4/pgstatstatements.html

INSTALL:
1. Clone the repo.
2. cd /path/pgtune/ pip install -e . 

HOW TO RUN:

Change the config.py db settings like host, port etc for your db

cmd: **pgtune**

It will generate a /tmp/pgtune.txt file with tuning logs. 

Example of txt file: 
```
----CONFIG related changes----

checkpoint_timeout should be increased or reduced based upon how frequently it is being called in your log.If called regularly, this would mean that the checkpoint is being reached sooner, mostly during bulk updates. And thus making the db flush data from memory into persistent storage, which would make updates slower. Recommended to increase if need be based upon amount of data being dumped.

wal_level can be turned into minimal if the database server has no replica running.


----Indexing required for these tables and columns----

table: test, columns: [{'colour', 'date'}]
table: test2, columns: [{'name'}]
```
Limitations/Enhancements needed:
1. Support for parent/child paritioned tables. 
2. Support for composite indexes. 
3. Understanding size of table, and query size to suggest better partitioning. 
4. Understanding no. of orderby and various other sorts to improve on work_mem suggestions.
5. Better understanding of queries to suggest CTEs and Views. 

