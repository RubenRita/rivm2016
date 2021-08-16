import sqlite3


class CreateDB:
    def __init__(self):
        self.database = "data.db"
        self.conn = sqlite3.connect(self.database)
        self.c = self.conn.cursor()
            
    def _create_indicators_table(self):
            msg = '''CREATE TABLE IF NOT EXISTS indicators(id integer primary key autoincrement not null, method varchar(45), category varchar(45), indicator varchar(45), unit varchar(45)) '''
            self.c.execute(msg)
            self.conn.commit()
            return None

    def _create_impacts_table(self):
            msg = '''CREATE TABLE IF NOT EXISTS impacts(id integer primary key autoincrement not null, indicator_id INTEGER, entry_id INTEGER,coefficient REAL, FOREIGN KEY(indicator_id) REFERENCES indicators(id), FOREIGN KEY(entry_id) REFERENCES entries(id)) '''
            self.c.execute(msg)
            self.conn.commit()
            return None
        
    def _create_entries_table(self):
            msg = '''CREATE TABLE IF NOT EXISTS entries(id integer primary key autoincrement not null, product_name varchar(255), unit varchar(45), geography_id varchar(45) REFERENCES geographies(id)) '''
            self.c.execute(msg)
            self.conn.commit()
            return None
        
    def _create_geographies_table(self):
            msg = '''CREATE TABLE IF NOT EXISTS geographies(id varchar(5) not null, short_name varchar(255), name varchar(45)) '''
            self.c.execute(msg)
            self.conn.commit()
            return None
        
    def _droptables(self,table):
        print(f'Removing Tables if Exist!')
        self.c.executescript(f'drop table if exists {table};')
        self.conn.commit()        
          
    def insert_indicators(self,recordList):
        self._droptables('indicators')
        print(f'Connected to {self.database}')
        self._create_indicators_table()
        msg = '''INSERT INTO indicators VALUES (NULL, ?,?,?,?) '''
        for record in recordList:
            t = (record['method'],record['category'],record['indicator'],record['unit'])       
            self.c.execute(msg,t)
            self.conn.commit()
        self.c.close()
        self.conn.close()
        return None
    
    def insert_entries(self,recordList):
        self._droptables('entries')
        print(f'Connected to {self.database} to entries')
        self._create_entries_table()
        msg = '''INSERT INTO entries VALUES (NULL, ?,?,?) '''
        for record in recordList:
            t = (record['product_name'],record['unit'],record['geography'])       
            self.c.execute(msg,t)
            self.conn.commit()
        self.c.close()
        self.conn.close()
        return None
    
    def insert_impacts(self,recordList):
        self._droptables('impacts')
        print(f'Connected to {self.database} to impacts')
        self._create_impacts_table()
        msg = '''INSERT INTO impacts VALUES (NULL, ?,?,?) '''
        for record in recordList:
            t = (record['indicator_id'],record['entries_id'],record['coefficient'])       
            self.c.execute(msg,t)
            self.conn.commit()
        self.c.close()
        self.conn.close()
        return None    
    
    def insert_geographies(self):
        self._droptables('geographies')
        print(f'Connected to {self.database} to geographies')
        self._create_geographies_table()
        msg = '''INSERT INTO geographies VALUES (?,?,?) '''
        t = ('NL','NLD','The Netherlands')       
        self.c.execute(msg,t)
        self.conn.commit()
        self.c.close()
        self.conn.close()
        return None

        
        
    