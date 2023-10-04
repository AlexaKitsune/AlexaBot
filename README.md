
# **AlexaBot** 🦊

# Hardware

This section will describe the electronic components used in the construction of AlexaBot and the connections between them, in addition to the mechanical specifications and the models available for 3D printing or some other form of manufacturing.
Also will describe the construction and set up of the physical parts.

## Electronic Component list

We will need the following components:

- x1 **MPU6050** sensor.
- x6 **MG90S** 180° servomotor.
- x1 **MG995** 180° servomotor.
- x1 **SS8050** transistor.

You will also need a computer to act as AlexaBot's brain.
We decided not to choose a Raspberry Pi because it fell short for some tasks (such as offline language processing).
However, you are free to choose one with similar or superior features. This computer will be where we will install the repository and where **installations** steps will take place.

## Schematic

```
                                 To "AlexaBot brain"          +5vcc
                                 ↑                            ↑
                                 │                            │                 220Ω
                                 │                     SS8050 │      UV LED ┌───\/\/\───┐
                              ┌──┴──┐          10kΩ     /-C───┘  ┌───|>|────┤   220Ω    │
 ┌────[PWR]───────────────────│ USB │──┐   ┌───\/\/\───┤B        │          └───\/\/\───┤
 │                            └─────┘  │   │            \-E──────┤              220Ω    │
 │         GND/RST2  [ ][ ]            │   │                     │   UV LED ┌───\/\/\───┤
 │       MOSI2/SCK2  [ ][ ]  A5/SCL[ ] │   │                     └───|>|────┤   220Ω    │
 │          5V/MISO2 [ ][ ]  A4/SDA[ ] │   │                                └───\/\/\───┤
 │                             AREF[ ] │   │                                            │
 │                              GND[ ] │   │                                            ↓ GND
 │ [ ]N/C                    SCK/13[ ] ├───┘           +5vcc                   +5vcc                   +5vcc                   +5vcc                   +5vcc                   +5vcc                   +5vcc
 │ [ ]IOREF                 MISO/12[ ] ├─────────────┐ ↑  _______ MG995        ↑  _______ MG90S        ↑  _______ MG90S        ↑  _______ MG90S        ↑  _______ MG90S        ↑  _______ MG90S        ↑  _______ MG90S  
 │ [ ]RST                   MOSI/11[ ]~├───────────┐ │ │  .┌─┴─────────┐.      │  .┌─┴─────────┐.      │  .┌─┴─────────┐.      │  .┌─┴─────────┐.      │  .┌─┴─────────┐.      │  .┌─┴─────────┐.      │  .┌─┴─────────┐.
 │ [ ]3V3    ┌───┐               10[ ]~├─────────┐ │ │ └───┤VCC        │       └───┤VCC        │       └───┤VCC        │       └───┤VCC        │       └───┤VCC        │       └───┤VCC        │       └───┤VCC        │ 
 │ [ ]5v    -│ A │-               9[ ]~├───────┐ │ │ └─────┤Signal     │       ┌───┤Signal     │       ┌───┤Signal     │       ┌───┤Signal     │       ┌───┤Signal     │       ┌───┤Signal     │       ┌───┤Signal     │ 
 │ [ ]GND   -│ R │-               8[ ] ├─────┐ │ │ │     ┌─┤GND        │       │ ┌─┤GND        │       │ ┌─┤GND        │       │ ┌─┤GND        │       │ ┌─┤GND        │       │ ┌─┤GND        │       │ ┌─┤GND        │ 
 │ [ ]GND   -│ D │-                    │     │ │ │ │     ↓ └───────────┘       │ ↓ └───────────┘       │ ↓ └───────────┘       │ ↓ └───────────┘       │ ↓ └───────────┘       │ ↓ └───────────┘       │ ↓ └───────────┘ 
 │ [ ]Vin   -│ U │-               7[ ] │───┐ │ │ │ └───────────────────────────┘                       │                       │                       │                       │                       │            
 │          -│ I │-               6[ ]~│─┐ │ │ │ └─────────────────────────────────────────────────────┘                       │                       │                       │                       │
 │ [ ]A0    -│ N │-               5[ ]~│ │ │ │ └───────────────────────────────────────────────────────────────────────────────┘                       │                       │                       │
 │ [ ]A1    -│ O │-               4[ ] │ │ │ └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘                       │                       │
 │ [ ]A2     └───┘           INT1/3[ ]~│ │ └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘                       │
 │ [ ]A3                     INT0/2[ ] │ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
 │ [ ]A4/SDA  RST SCK MISO     TX>1[ ] │
 │ [ ]A5/SCL  [ ] [ ] [ ]      RX<0[ ] │
 │            [ ] [ ] [ ]              │
 │  UNO_R3    GND MOSI 5V  ____________/
  \_______________________/

```

# Software

This section will describe the software organization, usage and installation.

## File organization:

```
AlexaBot/
├── 3d-models/
├── hardware/
├── src/
│   ├── image_recognition/
│   │   ├── models/
│   │   ├── qr_decode.py
│   │   └── yolo.py
│   ├── language_processing/
│   │   ├── models/
│   │   │   └── uncensored/
│   │   ├── chat_gpt.py
│   │   ├── llama_vicuna.py
│   │   ├── memory.py
│   │   └── tts.py
│   ├── memory/
│   │   ├── day-resumes/
│   │   ├── exp/
│   │   │   └── object-detection/
│   │   ├── week-resumes/
│   │   └── context.txt
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## 3D Models 📁
The `3d-models/` folder contains all the files for edit and 3d printing in .skp format.

## Hardware 📁
The `hardware/` folder includes all Arduino files for the electronic systems working, and the `alexa-bot.urdf` file for robotic simulation.

## Image recognition models 📁
The `src/image_recognition/models/` folder should contain the YOLOv8 models for image recognition.

The models recommended are the following:

- `yolov8m-cls.pt`
- `yolov8m-pose.pt`
- `yolov8m-seg.pt`
- `yolov8m.pt`
- `yolov8n-cls.pt`
- `yolov8n-pose.pt`
- `yolov8n-seg.pt`
- `yolov8n.pt`
- `yolov8x-cls.pt`
- `yolov8x-pose.pt`
- `yolov8x-seg.pt`
- `yolov8x.pt`

Those models will be downloaded automatically if not on the folder, but you can download it manually and view the YOLOv8 documentation on [github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics#models)

## Language processing models 📁
The `src/language_processing/models/` folder should contain the LLM models.

The models recommended are the following:

- `llama-2-13b-chat.ggmlv3.q2_K.bin`
- `llama-2-13b-chat.ggmlv3.q4_0.bin`
- `vicuna_llm_quantized.bin`

The first two models are available on [huggingface.co/TheBloke/Llama-2-13B-chat-GGML](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/).
The third model can be downloaded from [huggingface.co/ExploreWithYasir/vicuna_llm_quantized](https://huggingface.co/ExploreWithYasir/vicuna_llm_quantized).

You can also install other models. We have tried with:

- `Wizard-Vicuna-13B-Uncensored.ggmlv3.q2_K.bin`
- `Wizard-Vicuna-13B-Uncensored.ggmlv3.q4_0.bin`
- `Wizard-Vicuna-13B-Uncensored.ggmlv3.q8_0.bin`

Those models are available on [huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GGML](https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GGML/).


## Installation

Clone this repository in your working directory, and then move inside it.

> [!IMPORTANT]  
> This repository (or if you prefer, just the `src/` folder), must be located on the computer that will act as AlexaBot's brain.

```
cd AlexaBot
```

Move to `src/` folder. This directory will be the backend of AlexaBot (where the python project will be initiated / running).
```
cd src
```

Optional: create a virtual environment with:
```
py -3 -m venv venv
venv\Scripts\activate
```

Install python dependences.
```
pip install -r requirements.txt
```

Inside the `src/` folder, you will find a file named `config.json` with the following structure:
```json
[
    {
        "langProcessor": "llama_vicuna",
        "model": "vicuna_llm_quantized.bin",
        "gptApikey": "y0ur5up3r53cr374p1k3y",
        "YOLOsize": "n"
    }
]
```

You can configure it with your preferences:

- `langProcessor`: Is the name of the processor you will use. It can be only `llama_vicuna` or `chat_gpt`.
  - If you choose `llama_vicuna` you will need the LLM models inside your `language_processing/models/` folder, but if you choose `chat_gpt`, you will need an OpenAI API key.

- `model`: The name of the language model you will use.

- `gptApiKey`: Your API key from OpenAI to use Chat GPT.
  - Not necesary if you use `llama_vicuna` as langProcessor

- `YOLOsize`: Size of the YOLOv8 model for image recognition. It can be `n` for nano, `m` for medium or `x` for extra large.