import mysql.connector


class DbOps:

    def __init__(self, databaseName, tableName):
        '''
        :param databaseName:  Database Name
        :param tableName:  Table Name
        '''

        self.databaseName = databaseName
        self.tableName = tableName

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(user='username', password='password', host='localhost',
                                               database=self.databaseName)
            self.cursor = self.cnx.cursor()
            print("Connected to database successfully")
        except:
            print("Please check the database connection...")

    def database_exists(self):
        self.cursor.execute("SHOW DATABASES")
        print("Fetching Databases%%%%")
        result = self.cursor.fetchall()
        database_exists = False
        for x in result:
            if self.databaseName in x:
                database_exists = True
                break
        if database_exists:
            return True
        else:
            return False

    def createTable(self):
        query = "CREATE TABLE " + self.tableName + "( Keyword VARCHAR(255), SearchEngine VARCHAR(255), URLs VARCHAR(255), Title VARCHAR(255), Data TEXT);"
        self.cursor.execute(query)
        print("Created Table Successfully.......")

    def checkTable(self):

        # check if table exists
        query = "SHOW TABLES LIKE " + "'" + self.tableName + "'" + " ;"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            print("Table exists.")
            return True
        else:
            print("Table does not exist.")
            return False

    def insertQuery(self, Keyword, searchengine, URLs, Title, Data):
        sql = "INSERT INTO " + self.tableName + " ( Keyword, SearchEngine, URLs, Title, Data) VALUES (%s,%s,%s, %s, %s)"


        val = (Keyword,searchengine, URLs, Title, Data)
        self.cursor.execute(sql, val)
        self.cnx.commit()

        if self.cursor.rowcount >= 1:
            return True
        else:
            print("record not inserted")
            return False

    def searchKeyword(self, query):
        '''
        :param query: Keyword to search in database
        :return:
        '''

        sql = "SELECT * FROM " + self.tableName + " WHERE MATCH ( Keyword ) AGAINST ( '" +   query  + "') LIMIT 0, 30;"

        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        # print("Query Executed")
        results = [list(i) for i in res]
        return results

    def alterTable(self):
        sql ="ALTER TABLE "+ self.tableName + " ADD FULLTEXT(Keyword)"
        self.cursor.execute(sql)
        print("Set FULLTEXT Successfully")
