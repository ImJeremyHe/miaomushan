

class UserModel(object):
    def __init__(self, db):
        self.db = db
        self.table_name = "user"

    def get_user_by(self, condition, name):
        sql = 'SELECT * FROM %s WHERE %s = "%s"' % (self.table_name, condition, name)
        return self.db.query(sql)

    def add_new_user(self, user_account_info):
        sql = 'INSERT INTO %s (username, password, email, created) VALUES ("%s", "%s", "%s", "%s")' % \
              (self.table_name,
               user_account_info["username"], user_account_info["password"],
               user_account_info["email"], user_account_info["created"])
        return self.db.execute(sql)

    def authenticate(self, email, password):
        sql = 'SELECT * FROM %s WHERE email="%s" AND password="%s"' % (self.table_name, email, password)
        return self.db.query(sql)
