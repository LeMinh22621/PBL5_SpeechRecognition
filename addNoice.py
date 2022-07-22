import librosa
import os
from pydub import AudioSegment
import numpy as np
from pydub.generators import WhiteNoise
import soundfile as sf

import warnings
warnings.filterwarnings('ignore')

def addWhiteNoise(word, name):
    sound,sr = librosa.load(f"./DatasetV6/{word}/{name}", sr=44100)
    noise = np.random.normal(0, sound.std(), sound.size)
    augmented_signal = sound + noise*0.5
    sf.write(f"./DatasetV6.1/{word}/white_0.5_{name}", augmented_signal, sr)

def addBackgroundNoise(word, name):
    sound = AudioSegment.from_file(f"./DatasetV6/{word}/{name}")
    noice = AudioSegment.from_file("./Noise/DieuHoa.wav")
    combined = sound.overlay(noice)

    combined.export(out_f = f"./DatasetV6/{word}/background_noise{name}", format='wav')
def time_stretch(word, name):
    sound,sr = librosa.load(f"./DatasetV6/{word}/{name}")
    augmented_signal = librosa.effects.time_stretch(sound, 0.5)
    sf.write(f"./DatasetV6.1/{word}/time_0.5_{name}", augmented_signal, sr)


def createFile(word, name):
    isExist = os.path.exists(f"./DatasetV6.1/{word}")
    if not isExist:
        os.makedirs(f"./DatasetV6.1/{word}")
    # addBackgroundNoise(word, name)
    addWhiteNoise(word, name)
    time_stretch(word, name)

if __name__ == '__main__':
    class_names = ['Cua', 'Den', 'DieuHoa', 'Quat', 'Rem', 'TiVi']
    
    for cname in class_names:
        person = [i for i in os.listdir(os.path.join("DatasetV6",cname))
                                if i.endswith('.wav')]
        print("\t\t" + cname)
        for name in person:
            createFile(cname, name)