import sqlite3
from typing import List, Tuple

class UniversityORM:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_tables()
            self.populate_data()
        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}") 
        finally:
            self.conn.close()      

    
    def create_tables(self):
        if not self.table_exists('Students'):
            create_students_table = """
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER NOT NULL,
                city TEXT NOT NULL
            );
            """
            self.cursor.execute(create_students_table)
        
        if not self.table_exists('Courses'):
            create_courses_table = """
            CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time_start TEXT NOT NULL,
                time_end TEXT NOT NULL
            );
            """
            self.cursor.execute(create_courses_table)
        
        if not self.table_exists('Students_courses'):
            create_students_courses_table = """
            CREATE TABLE IF NOT EXISTS Students_courses (
                student_id INTEGER,
                courses_id INTEGER,
                FOREIGN KEY(student_id) REFERENCES Students(id),
                FOREIGN KEY(courses_id) REFERENCES Courses(id),
                PRIMARY KEY (student_id, courses_id)
            );
            """
            self.cursor.execute(create_students_courses_table)

    def table_exists(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        return self.cursor.fetchone() is not None

    def populate_data(self):
        try:
            courses_data = [
                ('python', '21.07.21', '21.08.21'),
                ('java', '13.07.21', '16.08.21')
            ]
            self.cursor.executemany("INSERT INTO Courses (name, time_start, time_end) VALUES (?, ?, ?)", courses_data)

            students_data = [
                ('Max', 'Brooks', 24, 'Spb'),
                ('John', 'Stones', 15, 'Spb'),
                ('Andy', 'Wings', 45, 'Manhester'),
                ('Kate', 'Brooks', 34, 'Spb')
            ]
            self.cursor.executemany("INSERT INTO Students (name, surname, age, city) VALUES (?, ?, ?, ?)", students_data)

            student_courses_data = [
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 2)
            ]
            self.cursor.executemany("INSERT INTO Students_courses (student_id, courses_id) VALUES (?, ?)", student_courses_data)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Данные уже существуют в базе")

    def close(self):
        self.conn.close()
    
    def get_students_over_age(self, age: int) -> List[Tuple]:
        query = """
        SELECT s.name, s.surname, s.age
        FROM Students s
        WHERE s.age > ?
        """
        self.cursor.execute(query, (age,))
        return self.cursor.fetchall()
    
    def get_students_by_course(self, course_name: str) -> List[Tuple]:
        query = """
        SELECT s.name, s.surname
        FROM Students s
        JOIN Students_courses sc ON s.id = sc.student_id
        JOIN Courses c ON sc.courses_id = c.id
        WHERE c.name = ?
        """
        self.cursor.execute(query, (course_name,))
        return self.cursor.fetchall()
    
    def get_students_by_course_and_city(self, course_name: str, city: str) -> List[Tuple]:
        query = """
        SELECT s.name, s.surname
        FROM Students s
        JOIN Students_courses sc ON s.id = sc.student_id
        JOIN Courses c ON sc.courses_id = c.id
        WHERE c.name = ? AND s.city = ?
        """
        self.cursor.execute(query, (course_name, city))
        return self.cursor.fetchall()