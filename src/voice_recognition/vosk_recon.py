from vosk import Model, KaldiRecognizer
import pyaudio


model = Model(r'./voice_recognition/models/vosk-model-es-0.42') #|vosk-model-en-us-0.22-lgraph
recognizer = KaldiRecognizer(model, 16000)
cap = pyaudio.PyAudio()
stream = cap.open(format = pyaudio.paInt16, channels = 1, rate = 16000, input = True, frames_per_buffer = 8192)


def listen():
    stream.start_stream()
    data = stream.read(1024, exception_on_overflow = False)
    if recognizer.AcceptWaveform(data):
        recognized = recognizer.Result().replace('{\n  "text" : "', '').replace('"\n}', '')
        #print(recognized)
        return recognized
