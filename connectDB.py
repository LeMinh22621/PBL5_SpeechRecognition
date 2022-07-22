import pyrebase


firebaseConfig = {
  'apiKey': "AIzaSyCdCBbf597UPVUN6XYoMRf8mRysZXJ23aw",
  'authDomain': "fir-pbl5.firebaseapp.com",
  'databaseURL': "https://fir-pbl5-default-rtdb.firebaseio.com",
  'projectId': "fir-pbl5",
  'storageBucket': "fir-pbl5.appspot.com",
  'messagingSenderId': "75188156157",
  'appId': "1:75188156157:web:4bb874793df15166243094",
  'measurementId': "G-2N52XNC63Y"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
datatat = {"TrangThai":"Off"}
databat = {"TrangThai":"On"}
data = db.child("ThietBi").child("Cua").child("TrangThai").get()
#db.child("ThietBi").child("Cua").update(datatat)
print(data.val())