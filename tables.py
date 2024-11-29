import sqlite3
import uuid
class table:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.commit()
            self.connection.close()
            self.connection = None
    def __del__(self):
        self.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"An error occurred: {exc_value}")
        self.close()
        
class credentials(table):
    def create(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS `login credentials` (
                `username` VARCHAR(16) NOT NULL,
                `email` VARCHAR(255) NULL,
                `password` VARCHAR(32) NOT NULL,
                `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (`username`),
                UNIQUE (`email`)
            )
        ''')
    def register(self,user,email,password):
        self.cursor.execute('''
            INSERT INTO `login credentials` (
                `username`,
                `email`, 
                `password`
            ) VALUES (?, ?, ?);
        ''',(user,email,password))
    def getUserDetails(self,user):
        self.cursor.execute('''
            SELECT `username`, `email`, `password`
            FROM `login credentials`
            WHERE `username` = ?;
        ''', (user,))
        return self.cursor.fetchone()

class sessions(table):
    def create(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS `Sessions` (
                `SessionID` TEXT PRIMARY KEY, 
                `username` TEXT NOT NULL,      
                `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (`SessionID`),
                FOREIGN KEY (`username`)
                    REFERENCES `login credentials` (`username`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
        ''')
    def login(self,user):
        sessionID = uuid.uuid4()
        self.cursor.execute('''
            INSERT INTO `Sessions` (
                `SessionID`,
                `username`
            ) VALUES (?, ?);
        ''',(sessionID,user))
        return sessionID
    def validate(self,sessionID,user):
        self.cursor.execute('''
            SELECT `username`
            FROM `login credentials`
            WHERE `SessionID` = ?;
        ''', (sessionID,))
        result = self.cursor.fetchone()
        return  result is not None and user == result[0]
        
    

