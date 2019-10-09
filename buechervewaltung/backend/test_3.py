"""

def checkerStatus(buehcer, id):
  #global res
  for buch in buehcer:
    pos = buch[5]
    pur = buch[0]
    if pur == id and pos== 'in':
      res= 'allowed'
      break

    else:
      res= 'not allowed'
      break

  return res

myresult= [(1,"System","Wil","Springer","09-19-2018","in"), (2,"Book","Bob","Springer Center","03-03-1999","in"), (3,"Book","Bob","Springer Center","03-03-1999","muster04@icloud.com") ]

print( checkerStatus(myresult,2))

for buch in myresult:
  pos= buch[5]
  pur= buch[0]
  if pos == 'in' and  pur == 2:
    print(buch)

"""
def checkStatus(query,id):
  res = list()
  for i in query:
    if i[0] == id and i[5]=='in':
      res.append(i)
      print(res)
  if len(res) >0:
    checker= 'free'
  else:
    checker= 'not free'
  return checker

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
myresult= [(1,"System","Wil","Springer","09-19-2018","in"), (2,"Book","Bob","Springer Center","03-03-1999","in"), (3,"Book","Bob","Springer Center","03-03-1999","muster04@icloud.com") ]
modeller = ('id', 'titel', 'autor', 'verlag', 'erscheinungsjahr', 'status')
email= "muster04@icloud.com"
email_2= 'in'
if checkStatus(myresult,1) == 'free':
  print( 'ja' )
else:
  print('nein')
print('fertig')
if checkerUser(myresult,3,email )== True:
  print('ja' )
else:
  print('nein')
