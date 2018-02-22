

class XzdzdModel(object):
    def __init__(self, db):
        self.db = db
        self.table = "earthquake"

    def get_records(self, t, c):
        sql = "SELECT name, t_%s, pga from %s WHERE type = %s" % (t, self.table, c)
        return self.db.query(sql)