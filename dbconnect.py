import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "",
                           port=3306,
                           db = "drugdiscover")
    c = conn.cursor()

    return c, conn		
def inserquery(sql1):
     c, conn = connection()
     c.execute(sql1)
     conn.commit()

     conn.close()
def inserquerypara(sql, params):
    c, conn = connection()
    # Your database connection code
    c.execute(sql, params)  # Use cursor to execute with parameters
    conn.commit()
    conn.close()
    # Your code to commit changes and close connection
def updatequery(sql1):
     c, conn = connection()
     c.execute(sql1)
     print(c.rowcount, "record(s) affected")
     conn.commit()
     conn.close()

def recoredselect(sql):
    c, conn = connection()
    c.execute(sql);
    result=c.fetchall();
    return result
