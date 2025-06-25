# 🧠 Face Recognition System

A real-time face recognition system built with Python, OpenCV, Tkinter, and MySQL.  
This GUI-based application allows users to register with personal details, capture face images from webcam, train a recognition model using LBPH, and recognize faces in real time — all while storing user data in a MySQL database managed through XAMPP.

---

## 🚀 Features

- GUI interface using Tkinter
- Face detection using Haar Cascade
- Dataset generation with webcam (200 grayscale images per user)
- Model training with LBPH Face Recognizer
- Real-time face recognition with live camera feed
- User data stored and retrieved from MySQL (via XAMPP)

---

## 💻 Tech Stack

- Language: Python
- Libraries: OpenCV, NumPy, Pillow, mysql-connector-python, Tkinter
- Model: LBPH Face Recognizer
- Database: MySQL (via XAMPP)
- Tools: VS Code, XAMPP, Git

---

## 📂 Project Structure

face-recognition-system/
├── main.py                           # Main app with GUI and logic  
├── gui_face_recognizer.ipynb         # Optional Jupyter version  
├── haarcascade_frontalface_default.xml  
├── requirements.txt  
├── README.md  

---

## ⚙️ Getting Started

### 1. Clone the Repository

git clone https://github.com/YourUsername/face-recognition-system.git  
cd face-recognition-system

### 2. Install Python Dependencies

pip install -r requirements.txt

---

## 🛢️ MySQL Setup using XAMPP

You must have XAMPP installed. Download from: https://www.apachefriends.org/index.html

### Steps:

1. Open XAMPP Control Panel
2. Start Apache and MySQL
3. Click "Admin" next to MySQL to open phpMyAdmin
4. In phpMyAdmin:
   - Click "New" to create a new database:
     authorized_user
   - Run the following SQL to create the required table:
     CREATE TABLE my_table (
         id INT PRIMARY KEY,
         Name VARCHAR(100),
         Age INT,
         Address VARCHAR(255)
     );

---

## ▶️ Run the Application

python main.py

---

## 🧠 How It Works

1. User Registration: Enter name, age, address via GUI.
2. Dataset Generation: App captures 200 images per user using webcam.
3. Model Training: LBPH Face Recognizer is trained with saved face data.
4. Real-time Recognition: Webcam feed is processed to identify known faces from trained model and database.

---

## 📝 Requirements

mysql-connector-python==8.0.33  
numpy==2.3.0  
opencv-contrib-python==4.11.0.86  
pillow==11.2.1

---

## 📄 License

This project is open-source and free to use under the MIT License.

---

## 👤 Author

Ralf Paul Victor  
GitHub: https://github.com/RalfVictor  
LinkedIn: https://www.linkedin.com/in/ralf-victor-10210b252/
