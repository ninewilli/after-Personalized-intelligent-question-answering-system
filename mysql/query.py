
import pymysql
import mysql.connector

# 创建连接

mydb=mysql.connector.connect(
	host="127.0.0.1", port=3306, user='root', passwd='fangyu2010',database="mysql"
)

mycursor = mydb.cursor()

def create_sql():
  try:
    mycursor.execute("CREATE TABLE user_map (id int(10),name varchar(10),question varchar(10),answer varchar(10),word varchar(10))")
  except:
    print("已创建")
  try:
    mycursor.execute("CREATE TABLE user_word (name varchar(10),mian_word varchar(10))")
  except:
    print("已创建")

def add_sql(id,name, question,answer,word):
  sql = "insert into user_map (id,name, question,answer,word) values ('%s','%s','%s','%s','%s')"%(id,name,question,answer,word)
  mycursor.execute(sql)
  mydb.commit()

def query(sql):
    mycursor.execute(sql)  # 执行查询sql 语句
    result = mycursor.fetchall()  # 记录查询结果
    return result 

def query_sql(word,name):
  sql = "select * from user_map where word='%s' and name!='%s'"%(word,name)
  tuple = query(sql)
  if len(tuple) != 0:
    print(tuple)

def consist():
  sql = "select * from user_map"
  tuple = query(sql)
  
