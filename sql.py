import sqlite3

# Connect to sqlite
connection = sqlite3.connect("student.db")

# Create a cursor object
cursor = connection.cursor()

# 1. Create the table
# Note: Using IF NOT EXISTS prevents errors if you run this multiple times
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25), 
    BRANCH VARCHAR(25), 
    SECTION VARCHAR(25), 
    MARKS INT
);
"""
cursor.execute(table_info)

# 2. Insert records (I included your full list here)
students = [
    ('Alice','Data Science','A', 98),
    ('Alice','Data Science','A',98),
    ('Bob','Computer Science','A',95),
    ('Charlie','Information Technology','B',88),
    ('David','Artificial Intelligence','A',92),
    ('Eva','Cyber Security','A',97),
    ('Frank','Data Science','C',74),
    ('Grace','Machine Learning','B',86),
    ('Hannah','Cloud Computing','A',93),
    ('Ian','Computer Science','B',84),
    ('Jasmine','Data Analytics','A',96),
    ('Kevin','Software Engineering','A',91),
    ('Linda','Data Science','B',89),
    ('Mike','Artificial Intelligence','C',73),
    ('Nina','Cyber Security','B',85),
    ('Oscar','Computer Science','A',94),
    ('Paul','Machine Learning','A',92),
    ('Queen','Data Analytics','B',87),
    ('Robert','Software Engineering','B',83),
    ('Sophia','Data Science','A',97),
    ('Tom','Cloud Computing','C',70),
    ('Uma','Cyber Security','A',95),
    ('Victor','Machine Learning','B',88),
    ('Wendy','Artificial Intelligence','A',90),
    ('Xavier','Software Engineering','C',76),
    ('Yara','Data Analytics','B',85),
    ('Zack','Computer Science','A',93),
    ('Aarav','Data Science','A',99),
    ('Bharat','AI & Robotics','B',86),
    ('Chitra','Machine Learning','A',96),
    ('Dev','Cyber Security','A',92),
    ('Esha','Cloud Computing','B',88),
    ('Farhan','Data Science','C',72),
    ('Gauri','Computer Science','B',85),
    ('Harsh','AI','A',90),
    ('Ishita','Data Analytics','A',94),
    ('Jay','Software Engineering','A',91),
    ('Kavya','Machine Learning','B',83),
    ('Laksh','Cyber Security','A',95),
    ('Mira','Data Science','B',89),
    ('Nikhil','Cloud Computing','C',78),
    ('Ovi','Data Analytics','A',93),
    ('Parth','Computer Science','B',82),
    ('Riya','AI','A',97),
    ('Sahil','Cyber Security','B',84),
    ('Tanvi','Machine Learning','A',96),
    ('Udit','Software Engineering','C',75),
    ('Vani','Data Science','A',94),
    ('Wasim','Artificial Intelligence','B',87),
    ('Xena','Cloud Computing','A',92),
    ('Yash','Computer Science','A',95),
    ('Zoya','Cyber Security','A',96),
    ('Aditya','Machine Learning','B',86),
    ('Bhavna','Software Engineering','A',90),
    ('Chetan','Data Analytics','B',88),
    ('Deepa','Computer Science','A',97),
    ('Ekansh','AI','B',82),
    ('Fatima','Data Science','A',95),
    ('Gautam','Cloud Computing','C',77),
    ('Heena','Machine Learning','A',96),
    ('Irfan','Cyber Security','B',84),
    ('Jiya','AI','A',93),
    ('Karan','Software Engineering','B',89),
    ('Leena','Data Science','A',99),
    ('Mohan','Computer Science','A',95),
    ('Naina','Data Analytics','B',87),
    ('Om','Machine Learning','A',94),
    ('Pooja','Cyber Security','A',92),
    ('Qadir','AI','C',74),
    ('Ritika','Software Engineering','A',91),
    ('Sameer','Cloud Computing','B',85),
    ('Tara','Data Science','A',96),
    ('Umesh','Computer Science','C',80),
    ('Veer','AI','A',98),
    ('Waseem','Machine Learning','B',88),
    ('Xain','Data Analytics','A',92),
    ('Yuvraj','Cyber Security','A',97),
    ('Zahid','Software Engineering','B',83),
    ('Ananya','Computer Science','A',96),
    ('Bunty','AI','B',85),
    ('Chandan','Cloud Computing','C',72),
    ('Dhruv','Machine Learning','A',94),
    ('Evan','Data Analytics','B',86),
    ('Fiona','Cyber Security','A',95),
    ('Gokul','Computer Science','B',82),
    ('Hans','AI','A',93),
    ('Indra','Software Engineering','A',91),
    ('Jatin','Data Science','B',90),
    ('Khushi','Machine Learning','A',97),
    ('Lalit','Cloud Computing','B',87),
    ('Meera','AI','A',98)
]

# Using executemany is cleaner and faster for bulk inserts
cursor.executemany('INSERT INTO STUDENT VALUES(?,?,?,?)', students)

# 3. Verify
print("Inserted records are:")
data = cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

# 4. CRITICAL FIX: Added parenthesis ()
connection.commit() 

connection.close()
