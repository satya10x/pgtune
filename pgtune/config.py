HOST = "127.0.0.1"
DB = "yogjadha"
PASSWORD = "xxx"
USER = "yogjadha"
PORT = "5432"
PG_VERSION=13  # PostgreSQL Major Version
# Default config
DEFAULT_CONFIG = {
	"work_mem": {"value": "4MB",
		"message": "**work_mem** value should be increased to make complex sorts(order by, distinct, merge joins) faster.\
A good value for work_mem can be Total RAM * 0.25 / max_connections"},
	"max_connections":  {"value": "100",
		"message" : "**max_connections** can be increased to support more connections,\
but ensure that work_mem * max_connections don't exceed RAM available else your db server would crash and burn."},
	"shared_buffers": {"value": "128MB",
		"message" : "Increasing **shared_buffers** would reduce time taken to read or write data as \
frequently queried datasets are stored in RAM. Ensure it remains 1/4th of your RAM as memory locked \
up by Postgres instance even when it might not get used."},
	"checkpoint_timeout": {"value": "30min",
		"message" : "**checkpoint_timeout** should be increased or reduced based \
upon how frequently it is being called in your log.\
If called regularly, this would mean that the checkpoint is being reached sooner, \
mostly during bulk updates. And thus making the db flush data from memory into persistent \
storage, which would make updates slower. Recommended to increase if need be based upon amount \
of data being dumped."},
	"wal_level": {"value": "replica",
		"message" : "**wal_level** can be turned into minimal if the database server has no replica running."},
	"auto_vaccuum": {"value": "ON",
		"message" : "**auto_vaccuum** can be turned off if frequent updates are happening of higher volume, as \
running vacuum during these updates can slow down. It would be better if vacuuming the entire \
database can be done through a cronjob at a suitable time when updates are less."
	}
}

#Config messages which will be exported to log
CONFIG_MESSAGES = {
	
}
# Queries
CONFIG_QUERY = "SHOW ALL"
PG_STAT_STATEMENT = "SELECT * FROM PG_STAT_STATEMENTS"
if PG_VERSION > 12:
	SLOW_QUERIES = "SELECT query FROM PG_STAT_STATEMENTS order by total_exec_time / calls limit 100"
else:
	SLOW_QUERIES = "SELECT query FROM PG_STAT_STATEMENTS order by total_time / calls limit 100"
HIGHEST_USED_QUERIES = "SELECT query FROM PG_STAT_STATEMENTS order by calls limit 100"
TABLE_INDEX_QUERY = """
						SELECT ARRAY_TO_STRING(ARRAY_AGG(a.attname), ', ') AS column_names
						FROM
						    pg_class t,
						    pg_class i,
						    pg_index ix,
						    pg_attribute a
						WHERE
						    t.oid = ix.indrelid
						    AND i.oid = ix.indexrelid
						    AND a.attrelid = t.oid
						    AND a.attnum = ANY(ix.indkey)
						    AND t.relkind = 'r'
						    AND t.relname =  %(table_name)s
						GROUP BY
						    t.relname,
						    i.relname
						ORDER BY
						    t.relname,
						    i.relname;
					"""