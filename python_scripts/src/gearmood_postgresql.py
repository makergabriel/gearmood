import psycopg2
import configparser
import os.path
from psycopg2.extras import Json
import env_config

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
        config = env_config.EnvConfig()
        try:
            self.conn = psycopg2.connect(
                "dbname='" + config.get_value("DatabaseSection","database.dbname") +
                "' user='" + config.get_value("DatabaseSection","database.user") +
                "' host='" + config.get_value("DatabaseSection","database.host") +
                "' password='" + config.get_value("DatabaseSection","database.password") +"'")
        except:
            print("Unexpected error:")
            raise
        table_exists(self.conn, "shake")
        table_exists(self.conn, "sentence")


    def save_shakedown(self, shakedown):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO shake (submission_id, subreddit_id, title, data) " +
                    "VALUES (%s, %s, %s, %s) " +
                    "ON Conflict (submission_id) DO UPDATE SET data = %s",
                    (shakedown["id"], shakedown["subreddit_id"],
                    shakedown["title"], Json(shakedown), Json(shakedown)))
        #print("Shakedown {} : {}".format(shakedown["title"], "https://www.reddit.com/" + shakedown["id"]))
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

    def save_sentence(self, submission_id, cut_sentences):
        cur = self.conn.cursor()
        for cut_sentence in cut_sentences:
            cur.execute("INSERT INTO cut_sentence (submission_id, words, sentence) " +
                        "VALUES (%s, %s, %s)",
                        #"ON Conflict (submission_id) DO UPDATE SET words = %s, sentence = %s",
                        (submission_id, Json(cut_sentence["words"]), cut_sentence["sentence"]))
        self.conn.commit()
        cur.close()
    
if __name__ == '__main__':
    GearMoodPS()