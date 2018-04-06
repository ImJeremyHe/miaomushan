

class XzdzdModel(object):
    def __init__(self, db):
        self.db = db
        self.table = "earthquake"

    def get_records(self, t, c, pga):
        sql = "SELECT name, t_%s, pga, magnitude, epid from %s WHERE type = %s and pga >= %s" % (t, self.table, c, pga)
        return self.db.query(sql)