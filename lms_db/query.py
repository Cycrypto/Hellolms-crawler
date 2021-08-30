import lms_db.__init__ as settings
import sqlite3


class Query:
    def __init__(self, db=settings.DB_PATH):    # 기본적인 데이터베이스 세팅
        self._conn = sqlite3.connect(db)
        self._cursor = self._conn.cursor()      # db 접근 커서 생성

    def createTable(self, name, *args):
        query = f"""
        CREATE TABLE {name} {args} 
        """
        # self._cursor.execute(query)
        print(query)

    def deleteTable(self):
        pass

    def insertData(self, name, *args):
        query = f"""
        INSERT INTO {name} VALUES {args} 
        """
        print(*query)
        self._cursor.execute(query)

    def __del__(self):
        print("class is end")
        self._conn.close()


if __name__ == "__main__":
    q = Query()
    q.createTable("a",'Date text',' Open int',' High int', 'Low int', 'Closing int', 'Volumn int')
    q.insertData("a", r'16.06.03', 97000, 98600, 96900, 98000)