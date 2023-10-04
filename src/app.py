#https://github.com/mdredze/carmen-python
import json
import schedule
import time
import os
from language_processing.tts import tts
from voice_recognition.vosk_recon import listen
from image_recognition.yolo import predict_vga
from image_recognition.process_image import process_image
from motor.head import eyes, jaw
from motor.connect import send_data

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
lang_processor = config_data[0]['langProcessor']

processors = {
    "chat_gpt": "language_processing.chat_gpt",
    "llama_vicuna": "language_processing.llama_vicuna"
}

if lang_processor in processors:
    module_path = processors[lang_processor]
    from importlib import import_module
    lang_module = import_module(module_path)
    chat = lang_module.chat
    reset_context_window = lang_module.reset_context_window
    resume = lang_module.resume


context_window = []
not_seeing_count = 0

def end_of_day_task():
    os.system("cls")
    print("DREAMING...")
    global context_window
    resume(context_window)
    reset_context_window()

schedule.every().day.at("12:00").do(end_of_day_task)

#count = 0 #<-testing.

def main_function(data_, img_):
    global not_seeing_count
    sensor_data = ""

    vision_data = process_image(data_, img_)
    if vision_data is not None:
        sensor_data += vision_data[0]
        send_data(eyes(vision_data[1]))
        not_seeing_count = 0
    else:
        not_seeing_count += 1
    print(not_seeing_count)
    if(not_seeing_count > 100):
        send_data({"difference_x":0, "difference_y": 0, "READY": 1})
        not_seeing_count = 0
        
        
    recognized = listen()
    if isinstance(recognized, str):
        if(recognized != ""):
            print("<<< ", recognized)
            completion = chat(recognized + " " + sensor_data)
            global context_window
            context_window = completion["context_window"]
            send_data(jaw(completion["reply"]))
            tts(completion["reply"])
            
    schedule.run_pending()


main_loop = predict_vga
if __name__ == "__main__":
    send_data({"READY": 1})
    time.sleep(0.5)
    send_data({"READY": 1})
    print("READY")
    
    main_loop(input_=0, save_=False, function_=main_function, show_=True)
