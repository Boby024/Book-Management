"""
from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime
app = Flask(__name__)


#Verbindung mit der Datenbank
mydb = mysql.connector.connect(
  host='localhost',
  user='Bob',
  passwd='Iamusing24@',
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM buecherverwaltung.users")
myresult = mycursor.fetchall()
print(myresult)

final_list= []
res={}
for test_keys in result:
  for key in test_keys:
    for value in test_values:
      res[key]=value
      test_keys.remove(value)
      break
  final_list.append(res)
print(final_list)

def prepareforJSON(listFromDB, modeller):
  final_list = []
  for first in listFromDB:
    final_list.append(dict(zip(modeller, first)))
  return final_list


result= [(1, 'alber@gmail.com', 'dsjkfnjWE323'), (5, 'azaza@icloud.com', 'booooooooojsdjhS'), (6, 'azaza@outlook.com', 'hhdjooooooooo'), (8, 'el fabr', 'passwortmuster00 '), (2, 'gerogo87@icloud.com', 'mSNAKJ232+@jk'), (7, 'muster01@yahoo.com', 'passwort01'), (4, 'yinyin34@icloud.com', 'ahju4762DKJS'), (3, 'yun342@yahoo.fr', 'jnnmxwo23skjjd')]
test_values=("id","email","passwort")
text= (1, 'alber@gmail.com', 'dsjkfnjWE323')
print( [dict( zip(test_values, text ) ) ])

final_list= []
for first in result:
  final_list.append( dict(zip(test_values,first)) )
print(final_list)

print( prepareforJSON(result,test_values) )
print('fertig')

from flask import Flask, jsonify, request
import mysql.connector
#from flaskext import MySQL
from flask_mysqldb import MySQL
from datetime import datetime
app = Flask(__name__)

#Verbindung mit der Datenbank
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'Bob'
app.config['MYSQL_PASSWORD']= 'Iamusing24@'
app.config['MYSQL_DB']= 'Buecherverwaltung'
mysql= MySQL(app)

cur = mysql.connection.cursor()
cur.execute("SELECT * FROM buecher WHERE titel = %s ","Job" )
myresult = cur.fetchall()


"""
