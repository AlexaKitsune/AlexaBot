# https://www.freecodecamp.org/news/how-to-detect-objects-in-images-using-yolov8/
from ultralytics import YOLO
import cv2, math


MODEL_PATH = "./image_recognition/models/"


def process_output(result):
    input_image = result.orig_img # Obtén la imagen original del resultado
    frame_height, frame_width, _ = input_image.shape # Obtiene las dimensiones del fotograma
    output = [{"frame": [frame_width, frame_height]}]
    for box in result.boxes:
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        x_min, y_min, x_max, y_max = cords
        center = [(x_min + x_max) / 2, (y_min + y_max) / 2]
        class_id = result.names[box.cls[0].item()]
        conf = round(box.conf[0].item(), 2)
        output.append({
            "objectType": class_id,
            "coordinates": cords,
            "center": center,
            "probability": conf
        })
    return output


def load_model(mode_, size_):
    # size_ can be < n | s | m |l | x >
    if(mode_ == "segment"):
        MODEL= f'yolov8{size_}-seg.pt'
    if(mode_ == "pose"):
        MODEL= f'yolov8{size_}-pose.pt'
    if(mode_ == "classify"):
        MODEL= f'yolov8{size_}-cls.pt'
    if(mode_ == "detect"):
        MODEL= f'yolov8{size_}.pt'
    return YOLO(MODEL_PATH + MODEL)


def predict_image(mode_="detect", input_="./bus.jpg", save_=True, size_="n", save_path="./memory/exp/object-detection/"):
    model = load_model(mode_, size_)
    results = model.predict(input_, save=save_, imgsz=320, conf=0.5, project=save_path) # predict on an image
    result = results[0]

    if(mode_ != "classify"):
        output = process_output(result)
        return output


def predict_video(mode_="detect", input_=0, save_=True, show_=True, size_="n", save_path="./memory/exp/object-detection/", function_=print):
    model = load_model(mode_, size_)
    results = model.predict(input_, save=save_, show=show_, project=save_path, imgsz=320, conf=0.5, stream=True, verbose=False) # predict on an image
    
    for result in results:
        if(mode_ != "classify"):
            output = process_output(result)
            # Each frame function here:
            function_(output, result.orig_img)


classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
            ]

def predict_vga(mode_="detect", input_=0, save_=True, show_=True, size_="n", save_path="./memory/exp/object-detection/", function_=print):
    model = load_model(mode_, size_)
    cap = cv2.VideoCapture(input_, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, img = cap.read()
        results = model.predict(img, save=save_, show=show_, project=save_path, imgsz=320, conf=0.5, stream=True, verbose=False)

        for result in results:
            if(mode_ != "classify"):
                output = process_output(result)
                # Each frame function here:
                function_(output, result.orig_img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()