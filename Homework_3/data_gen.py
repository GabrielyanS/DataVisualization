import sqlite3
import numpy as np
import time
from scipy import stats
import pandas as pd

connection = sqlite3.connect('data_db.db')
c = connection.cursor()
c.execute("DROP TABLE IF EXISTS dice_values")
c.execute("CREATE TABLE dice_values (id int, value1 int, value2 int,value3 int,value4 int,value5 int,value6 int,value7 int, mean float)")

c.execute("DROP TABLE IF EXISTS p_values")
c.execute("CREATE TABLE p_values (id int, p_value float)")

a = 0
i = 0
while i < 50:
	i += 1
	a = np.random.randint(1,7,7)
	mean = np.mean(a)
	c.execute("INSERT INTO dice_values values ({},{},{},{},{},{},{},{},{})".format(*np.append(np.append(i,a),mean)))
	connection.commit()
	query = ('SELECT * FROM dice_values')
	data = pd.read_sql_query(query, connection)
	mylist = data["mean"]
	if i >= 3:
		c.execute("INSERT INTO p_values values ({},{})".format(i,stats.shapiro(mylist)[1]))

	time.sleep(0.5)