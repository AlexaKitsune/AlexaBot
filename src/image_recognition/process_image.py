from image_recognition.qr_decode import qr_decode

def process_image(data_, img_):
    if(len(data_) == 1):
        return
    
    frame_size = data_.pop(0)["frame"]
    recognized_objects = data_
    phrase = ""

    sorted_by_size = sorted(recognized_objects, key=lambda x: (x['coordinates'][2] - x['coordinates'][0]) * (x['coordinates'][3] - x['coordinates'][1]))
    if sorted_by_size:
        smallest_object = sorted_by_size[0]  # El objeto más pequeño es el primero en la lista ordenada
        largest_object = sorted_by_size[-1]  # El objeto más grande es el último en la lista ordenada
    else:
        smallest_object = None
        largest_object = None
    sorted_objects = {
        "smaller_object": smallest_object,
        "bigger_object": largest_object,
        "all": sorted_by_size
    }

    for recon in recognized_objects:
        phrase += f'{recon["objectType"]} at {recon["center"]}, '

    QRs = qr_decode(img_)
    if(QRs != []):
        for qr in QRs:
            phrase += f'{qr["objectType"]} at {qr["center"]} with the content "{qr["QRcontent"]}", '

    result = f"(Vison/Image content: \n{phrase})"

    return [result, sorted_objects]
    #os.system("cls")
    #print(result, "\n")