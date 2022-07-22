
import os
import pickle
import wave
import numpy as np
import pyaudio
from pydub import AudioSegment
import preprocessing

import warnings

warnings.filterwarnings('ignore')

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
offCommand = {"TrangThai":"Off"}
onCommand = {"TrangThai":"On"}

class HMMRecognition:
    class_names = ['Cua', 'Den', 'DieuHoa', 'Quat', 'Rem', 'TiVi']
            # ['BatDen', 'BatDieuHoa', 'BatQuat', 'BatTiVi', 'DongCua', 'DongRem', 'MoCua', 'MoRem', 'TatDen', 'TatDieuHoa', 'TatQuat', 'TatTivi']
    def __init__(self):
        self.model = {}

        self.audio_format = 'wav'

        self.record_path = 'temp/record.wav'
        self.trimmed_path = 'temp/trimmed.wav'
        self.model_path = 'models_train'

        self.load_model()

    def load_model(self):
        for key in self.class_names:
            name = f"{self.model_path}/model_{key}.pkl"
            with open(name, 'rb') as file:
                self.model[key] = pickle.load(file)

    def predict(self, file_name=None):
        if not file_name:
            file_name = self.record_path
        # Predict
        record_mfcc = preprocessing.get_mfcc(file_name)
        scores = [self.model[cname].score(record_mfcc) for cname in self.class_names]
        
        predict_word = np.argmax(scores)
        print("\t" + file_name + " --> " + self.class_names[predict_word])

        device = self.class_names[predict_word]

        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()

        if(device == "Den"): #bat den
            data = db.child("ThietBi").child("Den").child("TrangThai").get()
            if(data.val() == "Off"):
                db.child("ThietBi").child("Den").update(onCommand)
            else:
                db.child("ThietBi").child("Den").update(offCommand)
        elif device == "TiVi":
            data = db.child("ThietBi").child("TiVi").child("TrangThai").get()
            if(data.val() == "Off"):
                db.child("ThietBi").child("TiVi").update(onCommand)
            else:
                db.child("ThietBi").child("TiVi").update(offCommand)
        elif device == "Quat":
            data = db.child("ThietBi").child("Quat").child("TrangThai").get()
            if(data.val() == "Off"):
                db.child("ThietBi").child("Quat").update(onCommand)
            else:
                db.child("ThietBi").child("Quat").update(offCommand)
        elif device == "DieuHoa":
            data = db.child("ThietBi").child("DieuHoa").child("TrangThai").get()
            if(data.val() == "Off"):
                db.child("ThietBi").child("DieuHoa").update(onCommand)
            else:
                db.child("ThietBi").child("DieuHoa").update(offCommand)
        elif device == "Cua":
            data = db.child("ThietBi").child("Cua").child("TrangThai").get()
            if(data.val() == "Off"):
                db.child("ThietBi").child("Cua").update(onCommand)
            else:
                db.child("ThietBi").child("Cua").update(offCommand)
        elif device == "Rem":
            data = db.child("ThietBi").child("Rem").child("TrangThai").get()
            if(data.val() == "Off"):
                db.child("ThietBi").child("Rem").update(onCommand)
            else:
                db.child("ThietBi").child("Rem").update(offCommand)
        
        return self.class_names[predict_word]
        
    def record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        print('recording ...')
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print('stopped record!')
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.record_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__ == '__main__':
    hmm_reg = HMMRecognition()
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    hmm_reg.record()
    tenthietbi = hmm_reg.predict()
    
    # print(tenthietbi)
    # if(tenthietbi == "Den"): #bat den
    #     data = db.child("ThietBi").child("Den").child("TrangThai").get()
    #     if(data.val() == "Off"):
    #         db.child("ThietBi").child("Den").update(databat)
    #     else:
    #         db.child("ThietBi").child("Den").update(datatat)
    # elif tenthietbi == "TiVi":
    #     data = db.child("ThietBi").child("TiVi").child("TrangThai").get()
    #     if(data.val() == "Off"):
    #         db.child("ThietBi").child("TiVi").update(databat)
    #     else:
    #         db.child("ThietBi").child("TiVi").update(datatat)
    # elif tenthietbi == "Quat":
    #     data = db.child("ThietBi").child("Quat").child("TrangThai").get()
    #     if(data.val() == "Off"):
    #         db.child("ThietBi").child("Quat").update(databat)
    #     else:
    #         db.child("ThietBi").child("Quat").update(datatat)
    # elif tenthietbi == "DieuHoa":
    #     data = db.child("ThietBi").child("DieuHoa").child("TrangThai").get()
    #     if(data.val() == "Off"):
    #         db.child("ThietBi").child("DieuHoa").update(databat)
    #     else:
    #         db.child("ThietBi").child("DieuHoa").update(datatat)
    # elif tenthietbi == "Cua":
    #     data = db.child("ThietBi").child("Cua").child("TrangThai").get()
    #     if(data.val() == "Off"):
    #         db.child("ThietBi").child("Cua").update(databat)
    #     else:
    #         db.child("ThietBi").child("Cua").update(datatat)
    # elif tenthietbi == "Rem":
    #     data = db.child("ThietBi").child("Rem").child("TrangThai").get()
    #     if(data.val() == "Off"):
    #         db.child("ThietBi").child("Rem").update(databat)
    #     else:
    #         db.child("ThietBi").child("Rem").update(datatat)