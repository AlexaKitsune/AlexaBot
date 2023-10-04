import pyttsx3

def tts(text_, rate_=150, save_=False):
    engine = pyttsx3.init() 
    # Control the rate. Higher rate = more speed
    engine.setProperty("rate", rate_)
    text = text_
    engine.say(text)

    if(save_):
        output_file = "./memory/exp/audio.mp3"
        engine.save_to_file(text, output_file)

    engine.runAndWait()