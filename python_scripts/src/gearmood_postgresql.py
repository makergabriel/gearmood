import psycopg2
import configparser
import os.path
from psycopg2.extras import Json

def table_exists(con, table_str):

    exists = False
    try:
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
        if exists:
            columns = get_table_col_names(con, table_str)
            print("Table {} exists with columns: {}".format(table_str, columns))
        
        cur.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def get_table_col_names(con, table_str):

    col_names = []
    try:
        cur = con.cursor()
        cur.execute("select * from " + table_str + " LIMIT 0")
        for desc in cur.description:
            col_names.append(desc[0])        
        cur.close()
    except psycopg2.Error as e:
        print(e)

    return col_names


class GearMoodPS:
    def __init__(self):
        config = configparser.ConfigParser()
        my_path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(my_path, "../config/gearmood-ps.ini")
        config.read(config_path)
        print(config.options("DatabaseSection"))
        db_section = config.options("DatabaseSection")
        dbname = config.get("DatabaseSection","database.dbname")
        print(db_section, dbname)
        try:
            self.conn = psycopg2.connect("dbname='" + config.get("DatabaseSection","database.dbname") +
            "' user='" + config.get("DatabaseSection","database.user") +
            "' host='" + config.get("DatabaseSection","database.host") +
            "' password='" + config.get("DatabaseSection","database.password") +"'")
        except:
            print("Unexpected error:")
            raise
        table_exists(self.conn, "shake")


    def save_shakedown(self, shakedown):
        cur = self.conn.cursor()
        cur.execute("INSERT into shake (subreddit_id, submission_id, title, data) values (%s, %s, %s, %s)",
                    (shakedown["subreddit_id"], shakedown["id"], shakedown["title"], Json(shakedown)))
        self.conn.commit()
        cur.close()

    def get_shakedown(self, submission_id):
        cur = self.conn.cursor()
        sql = "SELECT * FROM shake where submission_id = %s;"
        data = (submission_id, )
        cur.execute(sql,data)
        results = cur.fetchone()
        cur.close()
        return results
        
    def get_all_shakedowns(self):
        cur = self.conn.cursor()
        cur.execut("SELECT * FROM test;")
        result = cur.fetchall()
        print("result: {}".format(self))
        cur.close()
        return result
    
if __name__ == '__main__':
    GearMoodPS()