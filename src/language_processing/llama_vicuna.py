from llama_cpp import Llama
from language_processing.memory import save_day_resume
import re
import json


with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
llm_model = config_data[0]['model']
llm = Llama(model_path=f"./language_processing/models/{llm_model}", verbose=True, n_ctx=2048)


with open("./memory/context.txt", "r") as file:
    content = file.read()
CONTEXT_WINDOW = content


def chat(input_):
    global CONTEXT_WINDOW
    chat = llm(f"{CONTEXT_WINDOW} Q: {input_} A: ", stop=["Q:", "\n"], echo=True, max_tokens=2048)
    reply = remove_emojis(chat["choices"][0]["text"])
    CONTEXT_WINDOW = reply
    # Extract last answer:
    last_response = reply.split("A: ")
    last_response = last_response[len(last_response)-1]
    return {"reply":last_response, "context_window":reply}


def resume(input_):
    request = llm(f"AlexaBot, realiza un breve resumen del siguiente contenido, extrayendo los puntos más importantes. Recuerda que tú eres AlexaBot (asume el papel de AlexaBot): '{input_}' A: ", stop=["Q:", "\n"], echo=True)
    reply = request["choices"][0]["text"]
    save_day_resume(chat_to_json(input_), reply)
    print("SUMMARIZED + SAVED")
    return reply


def reset_context_window():
    global CONTEXT_WINDOW
    CONTEXT_WINDOW = content
    print("RESET CONTEXT WINDOW")


def chat_to_json(text):
    lines = text.split("\n")
    output = []

    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith("You are a"):
            output.append({"system": line})
        elif line.startswith("Q:"):
            question = {"Q": line[3:].strip()}
            output.append(question)
        elif line.startswith("A:"):
            answer = {"A": line[3:].strip()}
            output.append(answer)
    # Convertir la lista de diccionarios a formato JSON
    json_output = json.dumps(output, indent=4)
    
    return json_output

def remove_emojis(text):
    # Define el patrón de emojis utilizando una expresión regular
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticonos
                               u"\U0001F300-\U0001F5FF"  # símbolos y pictogramas
                               u"\U0001F680-\U0001F6FF"  # transportes y símbolos
                               u"\U0001F700-\U0001F77F"  # símbolos de alquimia
                               u"\U0001F780-\U0001F7FF"  # símbolos técnicos
                               u"\U0001F800-\U0001F8FF"  # símbolos numéricos
                               u"\U0001F900-\U0001F9FF"  # símbolos suplementarios y pictogramas
                               u"\U0001FA00-\U0001FA6F"  # emojis adicionales
                               u"\U00002702-\U000027B0"  # símbolos diversos
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)
    # Remueve los emojis del texto utilizando el patrón definido
    return emoji_pattern.sub(r'', text)