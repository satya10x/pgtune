from collections import defaultdict

import psycopg2
from pgtune.config import *
from pglast import Node, parse_sql

class PGTune():
	def __init__(self):
		self.conn = self._connect() # db connection
		self.cur = self.conn.cursor() # db cursor for that conn
		self.index_req = defaultdict(list)
		self.config_msgs = []

	def _connect(self):
		"""
			Connects db by picking config from
			config file and returns a db connection.
		"""
		return psycopg2.connect(
			host=HOST,
			database=DB,
			user=USER,
			password=PASSWORD,
			port=PORT)

	def _get_config_from_db(self):
		"""
			Fetches db config from the db itself
			rather than relying on parsing the config file
			as it would be difficult to get the config file
			from a remote server.
			Returns a dict of config
		"""
		config = defaultdict()
		self.cur.execute("{}".format(CONFIG_QUERY))
		for d in self.cur.fetchall():
			config[d[0]] = d[1]
		return config

	def inspect_pg(self):
		"""
			Check if pg_stat_statement is installed. 
			If not, ask the user to install and stop the
			tuning process.

			If pg_stat_statements exists, then do multiple
			analysis on it.

			* Fetch the top 10 slowest queries.
			* Fetch the top 10 highest queried tables.
		"""
		# check if pg_stat_statment module is there
		try:
			self.cur.execute("{}".format(PG_STAT_STATEMENT))
		except Exception:
			raise Exception("PG stat statement extension needs to be installed.")
		
		tables = defaultdict(list)

		self.cur.execute("{}".format(SLOW_QUERIES))
		for query in self.cur:
			tables.update(self._inspect_queries(query[0]))

		self.cur.execute("{}".format(HIGHEST_USED_QUERIES))
		for query in self.cur:
			tables.update(self._inspect_queries(query[0]))

		self._inspect_tables(tables)

	def _inspect_queries(self, query):
		"""
			Takes a query and creates a dict of metadata
			for each table that has table_name, and all its where
			clause columns.

			If encountered with a join query, make a separate entry
			for it.
			{"table_name": [x,y,z]}}
			returns a dict of tables that has a list of columns
		"""
		tables = defaultdict(list)
		try:
			root = Node(parse_sql(query))
			for node in root.traverse():
				try:
					if node.str:
						# Only store column names, and skip operators.
						if node.str.value not in ["=","<", ">", "!="]:
							tables[cur_rel].append(node.str.value)
					if node.relname:
						cur_rel = node.relname.value
						tables[cur_rel] = []
				except:
					pass
		except:
			"""
				NOTE: Syntax error caused by interval passing.
				I've not decided what's the best thing to do
				here, whether to fix the INTERVAL parsing, or
				do a string replace.
			"""
			pass
		pass

		return tables

	def _inspect_tables(self, tables):
		"""
			Fetches indexed columns of a table. 
			Then checks if the columns used in a query 
			are being indexed or not, and creates a 
			list out of these non-indexed columns.
		"""
		for tn, clms in tables.items():
			self.cur.execute("{}".format(TABLE_INDEX_QUERY), {"table_name": tn})
			clm_set = set(clms)
			# Loop through all columns, and remove any that's indexed.
			for tn_clm in self.cur:
				if tn_clm[0] in clm_set:
					clm_set.remove(tn_clm[0])
			if clm_set:
				self.index_req[tn].append(clm_set)

	def config_check(self):
		"""
		Fetches config of db. Checks with default config, 
		and see if basic tuning exists and suggests some more.
		"""
		for k, v in self._get_config_from_db().items():
			if k in DEFAULT_CONFIG.keys():
				if v in DEFAULT_CONFIG[k]["value"]:
					self.config_msgs.append(DEFAULT_CONFIG[k]["message"])

	def create_log(self):
		"""
			Creates a log temp file that can be read to
			understand and tune your postgres instance better.
		"""
		with  open("/tmp/pgtune.txt", "w") as pg_file:
			# Write to log file regarding all the config changes that
			# can be suggested
			pg_file.write("----CONFIG related changes----")
			pg_file.write("\n\n")
			for log in self.config_msgs:
				pg_file.write(log)
				pg_file.write("\n")
			pg_file.write("\n\n")	
			# Write to log file about all the indexing changes that can be done
			pg_file.write("----Indexing required for these tables and columns----")
			pg_file.write("\n\n")
			for k, v in self.index_req.items():
				pg_file.write("table: {}, columns: {}".format(k , v))
				pg_file.write("\n")

def run():
	pgtune = PGTune()
	s_flag = True
	try:
		pgtune.inspect_pg()
		pgtune.config_check()
		pgtune.create_log()
	except Exception as e:
		print(e)
		s_flag = False
	
	# Carry on with tuning if pg stat statements module exists
	if s_flag:
		pass

if __name__ == '__main__':
    run()