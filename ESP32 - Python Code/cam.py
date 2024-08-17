import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request

url = 'http://Ex:000.000.000.00/'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

font = cv2.FONT_HERSHEY_PLAIN  # Add this line to define the font

authorized_list = ['20230801', '20230802','20230803']  # Add your authorized data here

prev = ""
pres = ""
while True:
    img_resp = urllib.request.urlopen(url + 'cam-hi.jpg')
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        pres = obj.data.decode('utf-8')
        if prev == pres:
            pass
        else:
            print()
            print("Type:", obj.type)
            print("Data: ", obj.data)
            print("Student Roll No:", pres)
            prev = pres

            if pres in authorized_list:
                print("Authorized")
                authorized_message = "Authorized"
                color = (0, 255, 0)
            else:
                print("Un-Authorized")
                authorized_message = "Un-Authorized"
                color = (0, 0, 255)

        # Draw a box around the QR code
        pts = np.array(obj.polygon, dtype=np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, color, 5)
        text_position = (pts[0][0][0], pts[0][0][1] - 10)
        cv2.putText(frame, authorized_message, text_position, font, 1, color, 2)

    cv2.imshow("live transmission", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
