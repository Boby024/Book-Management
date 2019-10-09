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
