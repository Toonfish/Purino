import sqlite3 as sql
import settings

def getconn():
    conn = sql.connect(settings.server_path + 'invoiceDB.sqlite')
    return conn

def move_query(inv):
    return "UPDATE ER SET Pfade = '{}' WHERE RNr = '{}'".format(inv.get_pages_string(), str(inv.number))

def execute(query, sqlconn = None):
    print(query + "\n_____")  #temporary so I don't need the db
    return True
    if sqlconn:
        try:
            sqlconn.execute(query)
            return True
        except:
            return False
    else:
        try:
            sqlconn = getconn()
            sqlconn.execute(query)
            return True
        except:
            return False

def export_query(inv):
    query = "INSERT INTO ER VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '', '{6}', '{7}', {8}, {9}, null)"
    query = query.format(inv.number,
                         inv.date.sql_get(),
                         inv.cost_center,
                         inv.total_sum,
                         inv.vendor,
                         inv.scan_date.sql_get(),
                         inv.get_pages_string(),
                         inv.history,
                         inv.state,
                         inv.material)
    return query