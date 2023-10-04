from pyzbar.pyzbar import decode
import cv2
import numpy as np

def qr_decode(image):
    qr_codes = decode(image)

    qr_results = []

    for qr_code in qr_codes:
        qr_data = qr_code.data.decode('utf-8')
        qr_box = qr_code.polygon

        center = [(qr_box[0].x + qr_box[2].x) / 2, (qr_box[0].y + qr_box[2].y) / 2]
        cords = [qr_box[0].x, qr_box[0].y, qr_box[2].x, qr_box[2].y]

        qr_results.append({
            "objectType": "QR",
            "coordinates": cords,
            "center": center,
            "QRcontent": qr_data
        })

    return qr_results

# Ejemplo de uso
#image_path = 'path_to_your_image.jpg'
#image = cv2.imread(image_path)
#decoded_qrs = qr_decode(image)

#for qr in decoded_qrs:
#    print(qr)
