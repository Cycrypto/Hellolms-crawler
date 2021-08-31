import lms_db.__init__ as settings
import sqlite3


class Query:
    def __init__(self, db=settings.DB_PATH):  # 기본적인 데이터베이스 세팅
        self._conn = sqlite3.connect(db)
        self._cursor = self._conn.cursor()  # db 접근 커서 생성

    @staticmethod
    def joinString(*args, is_comma=True):
        qs = '('
        for idx, i in enumerate(args):
            qs += ''.join(i)
            if is_comma and idx < len(args) - 1:
                qs += ','
        qs += ')'
        return qs

    def createTable(self, name, *args):
        qs = self.joinString(*args, is_comma=True)
        query = f"""
        CREATE TABLE {name} {qs} 
        """
        self._cursor.execute(query)

    def deleteTable(self, name):
        query = f"DROP TABLE {name}"
        self._cursor.execute(query)

    def insertData(self, name, *args):
        qs = self.joinString(*args, is_comma=True)
        query = f"""
        INSERT INTO {name} VALUES{qs} 
        """
        self._cursor.execute(query)

    def __del__(self):
        print("class is end")
        self._conn.commit()
        self._conn.close()


if __name__ == "__main__":
    q = Query()
    # q.createTable("c", 'Date text', 'Open int', 'High int', 'Low int', 'Closing int', 'Volumn int')
    q.insertData("c", '\"16.06.03\"', '97000', '98600', '96900', '98000', '10400')
    q.deleteTable("c")