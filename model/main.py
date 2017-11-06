

class MainModel:
    def __init__(self, db):
        self.db = db
        self.essay_info_table_name = "essay_info"

    def get_essay_info_by_tid(self, tid):
        sql = "SELECT * FROM %s WHERE tid = %s" % (self.essay_info_table_name, tid)
        return self.db.query(sql)

    def create_essay(self, title, content, uid, username):
        sql = 'INSERT INTO %s (title, content, uid, username) VALUES ("%s", "%s", "%s", "%s")' % \
              (self.essay_info_table_name, title, content, uid, username)
        return self.db.execute(sql)



class MainRedisModel:
    def __init__(self, rd):
        self.rd = rd
        self.rd_hot_key = "hot_tid"

    def get_hottest_tid(self, num):
        return self.rd.zrevrange(self.rd_hot_key, 0, num)

    def add_hot_tid(self, tid, score):
        self.rd.zadd(self.rd_hot_key, tid, score)