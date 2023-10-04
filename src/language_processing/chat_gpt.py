import openai, json
from language_processing.memory import save_day_resume


with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
openai.api_key = config_data[0]['gptApikey']


with open("./memory/context.txt", "r") as file:
    content = file.read()
CONTEXT_WINDOW = [{"role":"system", "content":content}]


def chat(input_):
    CONTEXT_WINDOW.append({"role":"user", "content":input_},)
    #response:
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=CONTEXT_WINDOW)
    reply = chat.choices[0].message.content
    CONTEXT_WINDOW.append({"role":"assistant", "name":"AlexaBot", "content":reply})
    return {"reply":reply, "context_window":CONTEXT_WINDOW}


def resume(input_):
    request = [{"role":"system", "content": f"AlexaBot, realiza un breve resumen del siguiente contenido, extrayendo los puntos más importantes. Recuerda que tú eres AlexaBot (asume el papel de AlexaBot) : {input_}"}]
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=request)
    reply = chat.choices[0].message.content
    save_day_resume(input_, reply)
    return reply
    
    
def reset_context_window():
    global CONTEXT_WINDOW
    CONTEXT_WINDOW = [{"role":"system", "content":content}]
    