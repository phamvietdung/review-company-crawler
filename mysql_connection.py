import mysql.connector
from dotenv import load_dotenv
from common import get_hash
import os

load_dotenv()

mydb = mysql.connector.connect(
  host = os.getenv("MYSQL_HOST"),
  user = os.getenv("MYSQL_USER"),
  password = os.getenv("MYSQL_PASSWORD"),
  database = os.getenv("MYSQL_DATABASE")
)


mycursor = mydb.cursor()

create_table = """
CREATE TABLE Reviews 
(
	Id INT AUTO_INCREMENT PRIMARY KEY,
    CompanyName nvarchar(500) NULL,
    Salary nvarchar(500) NULL,
    Position nvarchar(500) NULL,
    `Year` nvarchar(500) NULL,
    Other nvarchar(2000) NULL,
    `Hash` nvarchar(100) NULL
)

CREATE TABLE `Logs`
(
	Id INT AUTO_INCREMENT PRIMARY KEY,
	`Data` nvarchar(2000) NULL,
    `Hash` nvarchar(100) NULL
)

CREATE TABLE Settings
(
	`Key` nvarchar(200) NOT NULL,
    `Value` nvarchar(200) NOT NULL
)

"""

# mycursor.execute(create_table)

def insert_review(CompanyName, Salary, Position, Year, Other, Hash):

    mycursor.execute("SELECT * FROM Reviews WHERE Hash = %s", (Hash,))
    if mycursor.fetchone() != None:
        # print("Review already exists, aborting")
        return

    sql = "INSERT INTO Reviews (CompanyName, Salary, Position, `Year`, Other, Hash) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (CompanyName, Salary, Position, Year, Other, Hash)
    mycursor.execute(sql, val)
    mydb.commit()

def get_reviews(page, page_size):
    mycursor.execute("SELECT * FROM Reviews LIMIT %s OFFSET %s", (page_size, page_size * (page - 1)))
    return mycursor.fetchall()

def get_review(id):
    mycursor.execute("SELECT * FROM Reviews WHERE Id = %s", (id,))
    return mycursor.fetchone()

def insert_log(data, hash):

    mycursor.execute("SELECT * FROM `Logs` WHERE Hash = %s", (hash,))
    if mycursor.fetchone() != None:
        return

    sql = "INSERT INTO `Logs` (`Data`, `Hash`) VALUES (%s, %s)"
    val = (data, hash)
    mycursor.execute(sql, val)
    mydb.commit()

def get_settings(key):
    mycursor.execute("SELECT * FROM Settings WHERE `Key` = %s", (key,))
    return mycursor.fetchone()

def set_settings(key, value):
    mycursor.execute("SELECT * FROM Settings WHERE `Key` = %s", (key,))
    if mycursor.fetchone() == None:
        sql = "INSERT INTO Settings (`Key`, `Value`) VALUES (%s, %s)"
        val = (key, value)
        mycursor.execute(sql, val)
    else:
        sql = "UPDATE Settings SET `Value` = %s WHERE `Key` = %s"
        val = (value, key)
        mycursor.execute(sql, val)
    mydb.commit()