from flask import Flask, jsonify, request
import mysql.connector
from _datetime import datetime

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

#hier füge ich key und values miteinander so, dass die Dekodierung als Json bei dem Frontend leichter wird
# modeller:("id","email","passwort") / ("id", "titel", "autor", "verlag", "erscheinungsjahr", "status")
def prepareforJSON(listFromDB, modeller):
  final_list = []
  for first in listFromDB:
    final_list.append(dict(zip(modeller, first)))
  return final_list


def checker_Contains(liste_db,parameter_1,parameter_2):
  my_list =[]
  for i in liste_db:
    if (i[1] == parameter_1 and i[2] == parameter_2):
      my_list.append((i[1], i[2]))

  # wenn die angegebenen Parameter mit den Inhalten von der DATENBANKEN überstimmen
  if (len(my_list) > 0):
    res='yes'
  else:
    res='no'
  return res

# wir chcecken hier, ob das Buch schon ausgeliehen ist, wenn ja retrun => True, wenn nein return => False
def checkStatus(query,id):
  res = list()
  for i in query:
    if i[0] == id and i[5]=='in':
      res.append(i)
  if len(res) >0:
    checker= 'free'
  else:
    checker= 'not free'
  return checker

# wir checken hier, ob der User erstens das Buch schon ausgeliehen hast, wenn ja => True, dann kann er das Buch zurückgeben,
# aber wenn nein => False, kann er das Buch nicht zurückgeben
def checkerUser(query,id, email):
  res = list()
  for i in query:
    if i[0] == id and i[5]== email:
      res.append(i)
      print(res)
  if len(res) >0:
    checker= True
  else:
    checker= False
  return checker

# diese Funktion gibt uns die Now time , damit man weiß, um wie viel der User das Buch ausgeliehen hast
def checkertime(query):

  if query >0 :
    gerade = datetime.now()
    # print(gerade)
    # print (str(gerade))

    ohneDezimal = str(gerade).split('.')
    # print (ohneDezimal)
    # print (ohneDezimal[0])
    datetime_object = datetime.strptime(ohneDezimal[0], '%Y-%m-%d %H:%M:%S')
    # print ( datetime_object)
    res= datetime_object
  else:
    res= '2000-01-01 00:00:00'

  return res

#Aufruf aller User , wenn es geprüft wird, ob der User im System existiert
@app.route('/api/users', methods=['GET'])
def all_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    result = cur.fetchall()
    cur.close()
    modeller=("id", "email", "passwort")
    final_result= prepareforJSON(result,modeller)
    #return result
    return jsonify(final_result)


# json file von Frontend beinhaltet (email und passwort), und dann wird der User in der Datenbank hinzugefügt
@app.route('/api/register', methods=['POST'])
def add_user():
  data= request.get_json()
  email = data['email']
  passwort = data['passwort']
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM users")
  list_users= cur.fetchall()
  if (checker_Contains(list_users,email,passwort)== 'no'):
    cur.execute("INSERT INTO users (email, passwort) VALUES (%s, %s)", (email, passwort))
    mysql.connection.commit()
    cur.close()
    result = {'message': 'register done', 'email' : email}
  else:
    result = {'message': 'register fail'}
  return jsonify(result)


# login() function nur wenn der User wirklich im System existiert
@app.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data['email']
  passwort= data['passwort']
  cur = mysql.connection.cursor()
  #cur.execute("SELECT * FROM users where email= %s", str(email) ) # ich nutze nur Email hier, weil die Emails in der Datenbanken als 'unique' sein muüssen
  cur.execute("SELECT * FROM users")
  list_users = cur.fetchall()
  cur.close()

  # ich checke in der Liste von allen User, ob der angegebenen Resquest(email and user ) in unserm System existiert
  #und wenn ja wird eine message mit 'done', wenn nein mit message 'fail'
  if(checker_Contains( list_users,email,passwort) == 'no'):
    result = {'message': 'login fail'}
  else:
    result = {'message': 'login done', 'email' : email}
  # wenn die Daten von User in der Liste steht => done
  # wenn nicht, => fail

  return jsonify(result)


#Aufruf aller User , wenn  sie gefragt werden
@app.route('/api/all_Buch', methods=['GET'])
def all_buch():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM buecher")
    result = cur.fetchall()
    cur.close()
    modeller = ("id", "titel", "autor", "verlag", "erscheinungsjahr", "status","ausgeliehen_am")
    #modeller = {"status", "titel", "id", "verlag", "titel", "erscheinungsjahr"}
    final_result = prepareforJSON(result,modeller)
    return jsonify(final_result)



# man fügt ein neues Buch in der Datenbank  (im System) hinzu
#Wir erwarten hier : titel, autor, verlag und ercheinungsjahr
@app.route('/api/add_buch', methods=['POST'])
def hinzufügen_buch():
  data = request.get_json()
  titel= data['titel']
  autor= data['autor']
  verlag= data['verlag']
  date_str= data['erscheinungsjahr']
  erscheinungsjahr = datetime.strptime(date_str, '%m-%d-%Y').date()
  val = (titel, autor, verlag, erscheinungsjahr)

  cur = mysql.connection.cursor()
  #Hier checke ich erstens, ob das Buch schon im System existiert (=> mit gleichen Eigenschaften)
  cur.execute("SELECT * FROM buecher")
  list_buecher = cur.fetchall()
  if (checker_Contains(list_buecher,titel,autor) == 'no'):
    cur.execute("INSERT INTO buecher (titel,autor, verlag, erscheinungsjahr) VALUES (%s,%s,%s,%s)",
                (titel, autor, verlag, erscheinungsjahr))
    mysql.connection.commit()
    cur.close()
    result = {'message': 'Buch added'}
  else:
    result= {'message': 'Buch already exists'} # wenn das Buch schon existiert , wird das System 'already' schicken

  return jsonify(result)


# Hier wird nur das ID des Buchs bekommen und dank diesem id wird das Buch mit ementsprechenden ID in der Datenbank (im System ) gelöscht
# Nur id des Buchs wird  beim Löschen erwartet
@app.route('/api/delete_buch', methods=['POST'])
def delet_buch():
  data = request.get_json()
  id= data['id']
  cur = mysql.connection.cursor()
  #response=cur.execute("DELETE FROM buecher where id = " + str(id) )
  response = cur.execute("DELETE FROM buecher where id = %s ", (id,) )
  # ALTER TABLE buecher AUTO_INCREMENT = id damit das 'id'- des Buchs für neue Bücher verfügbar wird
  #response_1= cur.execute("ALTER TABLE buecher AUTO_INCREMENT = " + str(id) )
  response_1 = cur.execute("ALTER TABLE buecher AUTO_INCREMENT = %s ",  (id,) )
  mysql.connection.commit()
  cur.close()

  # wenn das Delete funktioniert, dann wird 'response = 1 '
  if response > 0:
    result = {'message': 'buch deleted'}
    #result = {'message': 'buch deleted', 'response': response}
  else:
    result = {'message': 'buch not exist'}
  return jsonify( result )


#noch nicht gut
# id -buch und email des Users werden erwartet
@app.route('/api/buch_out', methods=['PUT'])
def ausleihen():
  data = request.get_json()
  email= data['email']
  id= data['id']

  # im System sind 02 status zu erkenen: 'in': neues Buch oder zurückgegeben und dann einfach die email-adresse (von der User , der das Buch ausgeliehen hast )
  # hier kriegen wir eine Liste von allen Buecher (id, titel,autor,verlag,erscheinungsjahr, status )
  cur = mysql.connection.cursor()
  #response= cur.execute("SELECT * FROM buecher WHERE status = %s " , email )
  cur.execute("SELECT * FROM buecher")
  myresult = cur.fetchall()

  # hier rechnen wir einfach nur wie viel Bücher den User schon ausgeliehen hat und vergleichen wir, ob das unter 4 ist
  list_out = []
  for each_list in myresult:
    # position_status[5] : denn in der Tabelle buehcer ist status in der 6. Spalte
    # print(each_list)
    status = each_list[5]
    # print(status)
    if status == email:  # nur email weil die Email 'unique' sind.
      list_out.append(status)

  # wenn der User(mitgilfe seiner Email) unter 4 Bücher ausgeliehen hat, dann aktualisieren wir den Status des Buchs im System mit seinem email.
  if len(list_out )< 3 and checkStatus(myresult,int(id) )== 'free':
    # cur.execute("UPDATE buecher SET stauts = %s WHERE  id = %s ", (email, id))
    response = cur.execute("UPDATE buecher SET status = %s  WHERE  id = %s ", (email, id))
    query= checkertime(response)
    cur.execute("UPDATE buecher SET ausgeliehen_am = %s  WHERE  id = %s ", (query,id))
    mysql.connection.commit()
    cur.close()

    # ich schicken hier 'done'  als response wenn die Function ausleihen funktioniert hat und wenn nicht 'fail'
    #result = {'ausgeliehen': 'done'}
    if response > 0:
      result_1 = {'ausgeliehen': 'done'}
    else:
      result_1 = {'ausgeliehen': 'fail'}
    result = result_1
  else:
    result = {'ausgeliehen': ' max 3 books'}

  return jsonify(result)


#noch nicht gut
# Nur id -buch wird  erwartet
@app.route('/api/buch_in', methods=['PUT'])
def zurueckgeben():
  data = request.get_json()
  id= data['id']
  email= data['email']
  status='in'
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM buecher")
  query= cur.fetchall()

  # damit dei Rückgabe-Urhzeit gesehen wird, habe ich einfach das Datum nicht auf 'NULL' zurücksetzen
  if checkerUser(query,id,email)== True :
    response= cur.execute("UPDATE buecher SET status= %s  WHERE id = %s ",(status, id) )
    mysql.connection.commit()
    cur.close()

    if response > 0:
      result_1 = {'zurueckgegeben': 'done'}
    else:
      result_1 = {'zurueckgegeben': 'fail'}
    result= result_1
  else:
    result= {'zurueckgegeben': 'not the same user'}
  return jsonify(result)


if __name__ == '__main__':
    app.run(port=5001, debug=True)


# test mit mysql.connector , also für normales python nutzung ohne Flask
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

# json file von Frontend beinhaltet (email und passwort), und dann wird der User in der Datenbank hinzugefügt
@app.route('/api/addUser', methods=['POST'])
def add_user():
  data= request.get_json()
  email = data['email']
  passwort = data['passwort']
  mycursor = mydb.cursor()
  sql = "INSERT INTO buecherverwaltung.users (email, passwort) VALUES (%s, %s)"
  val = (email, passwort)
  mycursor.execute(sql, val)
  mydb.commit()

  result={'message':'done'}
  return jsonify(data)


# login() function nur wenn der User wirklich im System existiert
@app.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data['email']
  passwort= data['passwort']
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM buecherverwaltung.buecher where status=" + email)
  myresult = mycursor.fetchall()

  # ich checke in der Liste von allen User, ob der angegebenen Resquest(email and user ) in unserm System existiert
  #und wenn ja wird eine message mit 'done', wenn nein mit message 'fail'
  my_list = []
  for i in myresult:
    if (i[1] == email and i[2] == passwort):
      my_list.append((i[1], i[2]))

  # wenn die Daten von User in der Liste steht => done
  # wenn nicht, => fail
  if( len( my_list) >0 ):
    result = {'message': 'done'}
    return jsonify(result)
  else:
    result = {'message': 'fail'}
    return jsonify(result)


#Aufruf aller User , wenn es geprüft wird, ob der User im System existiert
@app.route('/api/all_Users', methods=['GET'])
def all_users():
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM users")
  myresult = mycursor.fetchall()
  #print(myresult)
  return jsonify(myresult)


#Aufruf aller User , wenn  sie gefragt werden
@app.route('/api/all_Buch', methods=['GET'])
def all_buch():
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM buecherverwaltung.buecher")
  myresult = mycursor.fetchall()
  return jsonify(myresult)


# man fügt ein neues Buch in der Datenbank  (im System) hinzu
#Wir erwarten hier : titel, autor, verlag und ercheinungsjahr
@app.route('/api/add_buch', methods=['POST'])
def hinzufügen_buch():
  data = request.get_json()
  titel= data['titel']
  autor= data(['autor'])
  verlag= data(['verlag'])
  date_str= data(['ercheinungsjahr'])
  ercheinungsjahr = datetime.strptime(date_str, '%m-%d-%Y').date()
  mycursor = mydb.cursor()
  sql = "INSERT INTO buecherverwaltung.buecher (titel,autor, verlag, ercheinungsjahr) VALUES (%s, %s,%s,,%s,)"
  val = (titel,autor,verlag, ercheinungsjahr )
  mycursor.execute(sql, val)
  mydb.commit()

  result = {'message': 'done'}
  return jsonify(result)


# Hier wird nur das ID des Buchs bekommen und dank diesem id wird das Buch mit ementsprechenden ID in der Datenbank (im System ) gelöscht
# Nur id des Buchs wird  beim Löschen erwartet
@app.route('/api/one_buch/', methods=['POST'])
def delet_buch():
  data = request.get_json()
  id= data['id']
  mycursor = mydb.cursor()
  response=mycursor.execute("DELETE FROM buecherverwaltung.buecher where id= "+id )
  mydb.commit()

  if response > 0:
    result = {'message': 'record delete'}
  else:
    result = {'message': 'no record found'}

  return jsonify({'result': result})


# id -buch und email des Users werden erwartet
@app.route('/api/status/out', methods=['POST'])
def ausleihen():
  data = request.get_json()
  email= data['email']
  id= data['id']

  # im System sind 02 status zu erkenen: 'in': neues Buch oder zurückgegeben und dann einfach die email-adresse (von der User , der das Buch ausgeliehen hast )
  # hier kriegen wir eine Liste von allen Buecher (id, titel,autor,verlag,erscheinungsjahr, status )
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM buecherverwaltung.buecher where status="+email)
  myresult = mycursor.fetchall()

  # hier rechnen wir einfach nur wie viel Bücher den User schon ausgeliehen hat und vergleichen wir, ob das unter 4 ist
  list_out=[]
  for i in myresult:
    #position_status[5] : denn in der Tabelle buehcer ist status in der 6. Spalte
    position_status = i[5]
    if position_status == email :
      list_out.append(position_status)

  # wenn der User(mitgilfe seiner Email) unter 4 Bücher ausgeliehen hat, dann aktualisieren wir den Status des Buchs im System mit seinem email.
  if len(list_out <4 ):
    mycursor.execute("UPDATE buecherverwaltung.buecher SET stauts=' "+str(email)+" ' WHERE id=" +id )
    mydb.commit()

    #ich schicken hier 'done'  als response wenn die Function ausleihen funktioniert hat und wenn nicht 'fail'
    result= {'ausgeliehen': 'done' }
    return jsonify(result)
  else:
    result = {'ausgeliehen': 'fail'}
    return jsonify(result)


# Nur id -buch wird  erwartet
@app.route('/api/status/in', methods=['POST'])
def zurueckgeben():
  data = request.get_json()
  id= data['id']
  mycursor = mydb.cursor()
  mycursor.execute("UPDATE buecherverwaltung.buecher SET stauts=' " + str('in') + " ' WHERE id=" + id)
  mydb.commit()

  result= {'zurueckgegeben':'done'}
  return jsonify(result)



if __name__ == '__main__':
    app.run(port=5001, debug=True)


"""
