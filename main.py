import tkinter as tk
from tkinter import messagebox
import cv2
import os
from PIL import Image
import numpy as np
import mysql.connector

window = tk.Tk()
window.title("Face Recognition System")

# Labels and Entry fields
l1 = tk.Label(window, text="Name", font=("Algerian", 20))
l1.grid(column=0, row=0)
t1 = tk.Entry(window, width=50, bd=2)
t1.grid(column=1, row=0)

l2 = tk.Label(window, text="Age", font=("Algerian", 20))
l2.grid(column=0, row=1)
t2 = tk.Entry(window, width=50, bd=2)
t2.grid(column=1, row=1)

l3 = tk.Label(window, text="Address", font=("Algerian", 20))
l3.grid(column=0, row=2)
t3 = tk.Entry(window, width=50, bd=2)
t3.grid(column=1, row=2)

def generate_dataset():
    if t1.get() == "" or t2.get() == "" or t3.get() == "":
        messagebox.showinfo("Result", "Please Fill Every Field")
        return
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="authorized_user"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM my_table")
    myresult = mycursor.fetchall()
    id = len(myresult) + 1

    sql = "INSERT INTO my_table (id, Name, Age, Address) VALUES (%s, %s, %s, %s)"
    val = (id, t1.get(), t2.get(), t3.get())
    mycursor.execute(sql, val)
    mydb.commit()

    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            return img[y:y+h, x:x+w]

    cap = cv2.VideoCapture(0)
    img_id = 0

    while True:
        ret, frame = cap.read()
        cropped = face_cropped(frame)
        if cropped is not None:
            img_id += 1
            face = cv2.resize(cropped, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = f"data/user.{id}.{img_id}.jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Cropped face", face)

        if cv2.waitKey(1) == 13 or img_id == 200:
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Result", "Generating Dataset Completed.")

def train_classifier():
    data_dir = "C:/AI/Face Recognition/data"
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])
        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("Classifier.xml")
    messagebox.showinfo("Result", "Training Dataset Completed")

def detect_face():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray, scaleFactor, minNeighbors)
        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            id, pred = clf.predict(gray[y:y+h, x:x+w])
            confidence = int(100 * (1 - pred / 300))

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="authorized_user"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT Name FROM my_table WHERE id=" + str(id))
            result = mycursor.fetchone()
            name = ''.join(result) if result else "Unknown"

            if confidence > 80:
                cv2.putText(img, name, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
            else:
                cv2.putText(img, "Unknown", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            coords = [x, y, w, h]
        return img

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("Classifier.xml")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, img = video_capture.read()
        if not ret:
            print("Failed to read from camera.")
            break
        img = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
        cv2.imshow("Face Detection", img)

        if cv2.waitKey(1) == 13:
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Buttons with unique variable names
btn_train = tk.Button(window, text="Training", font=("Algerian", 20), bg="black", fg="white", command=train_classifier)
btn_train.grid(column=0, row=4)

btn_detect = tk.Button(window, text="Detect Face", font=("Algerian", 20), bg="black", fg="lime", command=detect_face)
btn_detect.grid(column=1, row=4)

btn_generate = tk.Button(window, text="Generate Dataset", font=("Algerian", 20), bg="black", fg="yellow", command=generate_dataset)
btn_generate.grid(column=2, row=4)

window.geometry("800x200")
window.mainloop()