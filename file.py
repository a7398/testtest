import sqlite3

# Создаем соединение с базой данных
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Создаем таблицу Students
create_students_table = """
CREATE TABLE Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL
);
"""
cursor.execute(create_students_table)

# Создаем таблицу Courses
create_courses_table = """
CREATE TABLE Courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time_start TEXT NOT NULL, 
    time_end TEXT NOT NULL
);
"""
cursor.execute(create_courses_table)

# Создаем таблицу Student_courses
create_student_courses_table = """
CREATE TABLE Student_courses (
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY(student_id) REFERENCES Students(id),
    FOREIGN KEY(course_id) REFERENCES Courses(id),
    PRIMARY KEY (student_id, course_id)
);
"""
cursor.execute(create_student_courses_table)

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()                  