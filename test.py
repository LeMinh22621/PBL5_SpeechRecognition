import pyrebase
import os
from hmm_predict import HMMRecognition
import time

config = {
    "apiKey": "AIzaSyCdCBbf597UPVUN6XYoMRf8mRysZXJ23aw",
    "authDomain": "fir-pbl5.firebaseapp.com",
    "projectId": "fir-pbl5",
    "databaseURL":"https://fir-pbl5-default-rtdb.firebaseio.com",
    "storageBucket": "fir-pbl5.appspot.com",
    "messagingSenderId": "75188156157",
    "appId": "1:75188156157:web:4bb874793df15166243094",
    "measurementId": "G-2N52XNC63Y"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()
path_on_cloud = "DatasetV6"
count = 0

if __name__ == "__main__":
    class_names = ['Cua', 'Den', 'DieuHoa', 'Quat', 'Rem', 'TiVi']

    while(True):
        try:
            storage.child("File/record.wav").download("","temp/record.wav")
            hmm_reg = HMMRecognition()
            hmm_reg.predict()
            os.remove('temp/record.wav')
            storage.delete("File/record.wav","Hi")
            count += 1
            print(count)
        except:
            time.sleep(1)

        