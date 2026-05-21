import pymysql
import config

class Database:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Database connected successfully!")
        except pymysql.MySQLError as e:
            print(f"Database connection failed! {e}")
    
    def get_cursor(self):
        return self.connection.cursor()
    
    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()