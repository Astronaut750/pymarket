import db

conn = db.open()
cursor = conn.cursor()
symbol = "tsla"
values = ("9.9", "2021-03-05")

sql = "UPDATE " + symbol + " SET average200 = "+ values[0] +" WHERE date = \""+ values[1] +"\";"
cursor.execute(sql)
conn.commit()