import sqlite3


class DataBase:
    # Create the constructor that will be called with the creation of any object of this class
    def __init__(self, db):
        # the below are names of variables(attributes):
        self.conn = sqlite3.connect(db)
        # 'Cursor' is used to excute queries
        self.cur = self.conn.cursor()
        # Make some fresh tables using executescript()
        self.cur.executescript(''' 

        CREATE TABLE IF NOT EXISTS patients(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name VARCHAR(80), l_name VARCHAR(80), phone CHARACTER(11),
        nationalId CHARACTER(14) NOT NULL UNIQUE, birthYear DATE, job VARCHAR(200), city VARCHAR(80), street VARCHAR(80), 
        gender CHARACTER(6), history TEXT
        );

        CREATE TABLE IF NOT EXISTS patient_treatment(patientId  INTEGER NOT NULL , visitDate DATE, treatment TEXT);
        
        ''')
        
        self.conn.commit()
        

    def fetch(self):
        self.cur.execute("SELECT * FROM patients")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, l_name, phone, nationalId, birthYear, job, city, street, gender, history):
        self.cur.execute('INSERT INTO patients VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, l_name, phone, nationalId, birthYear, job, city, street, gender, history))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute('DELETE FROM patients WHERE id=?', (id,))
        self.conn.commit()

    def update(self, id, name, l_name, phone, nationalId, birthYear, job, city, street, gender, history):
        self.cur.execute('UPDATE patients SET name = ?, l_name = ?, phone = ?, nationalId = ?, birthYear = ?, job = ? , city = ?, street = ?, gender = ?, history = ? WHERE id = ?',
                         (name, l_name, phone, nationalId, birthYear, job, city, street, gender, history, id))
        self.conn.commit()


    # Create a deconstructor :-
    def __del__(self):
        self.conn.close()