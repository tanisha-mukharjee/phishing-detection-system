# 🛡️ AI-Powered Phishing Detection System  
A machine-learning powered web application that detects phishing URLs in real-time using Flask, Scikit-Learn, and MongoDB Atlas.

---

## 📌 Project Overview  
This system analyzes URLs using multiple intelligent features like HTTPS usage, suspicious keywords, domain structure, IP-based URLs, and more.  
It then predicts whether a website is:

✔ **Legitimate**  
❌ **Phishing / Fraudulent**

The project includes:

- 🌐 Flask Web Interface  
- 🤖 Machine Learning Model (Random Forest)  
- ☁ MongoDB Atlas Logging  
- 📊 Admin Dashboard with URL History  
- 🎨 Clean UI (HTML5 + CSS3)

---

## 🚀 Live Demo (optional)
👉 *(Add your Render link here after deployment)*  
Example:  
`https://phishing-detector.onrender.com`

---

## 📸 Screenshots  

### 🏠 Home Page  
*(Insert screenshot of index.html)*  
![Home Page](screenshots/home.png)

### 🔍 URL Detection Result  
*(Insert screenshot of result.html)*  
![Result Page](screenshots/result.png)

### 📊 Admin Dashboard  
*(Insert screenshot of dashboard.html once ready)*  
![Dashboard](screenshots/dashboard.png)



## 🧠 Features  
| Feature | Description |
|--------|-------------|
| 🔍 Real-Time Prediction | Classifies URLs instantly |
| 🤖 ML Model | Trained using Random Forest |
| 🧪 Feature Extraction | URL length, IP address, HTTPS, keywords, etc. |
| ☁ Cloud DB | MongoDB Atlas stores all predictions |
| 📊 Dashboard | Admin panel shows logs & history |
| 🎨 Modern UI | Clean interface with HTML/CSS |


## 🛠️ Tech Stack

### **Backend**
- Python
- Flask
- Gunicorn (for deployment)

### **Machine Learning**
- Scikit-Learn  
- Pandas  
- NumPy  

### **Database**
- MongoDB Atlas (Cloud NoSQL)

### **Frontend**
- HTML5  
- CSS3  
- Jinja Templates  

---

## 🧮 How It Works (Flow Diagram)


User Enters URL → Feature Extraction → ML Model Predicts → Save in MongoDB → Show Result → (Optional) View Dashboard



## 🏗️ Installation & Running Locally

### 1️⃣ Clone the repository
bash
git clone https://github.com/<your-username>/phishing-detection.git
cd phishing-detection

### 2️⃣ Install dependencies
bash
pip install -r requirements.txt


### 3️⃣ Add MongoDB connection string  
Create `.env` file (optional):

MONGO_URI=your-atlas-connection-string

### 4️⃣ Run the Flask App  
bash
python app/app.py


### 🔗 Visit:

http://127.0.0.1:5000


## 🧠 Machine Learning Model  
The model is trained using the **Random Forest Classifier** on a dataset of phishing and legitimate URLs.

**Model Features Used:**
- URL length  
- Presence of '@'  
- HTTPS usage  
- Number of digits  
- Hyphens count  
- Dots count  
- Suspicious keywords  
- IP address usage  
- Domain length  

The trained model is saved as:  
`/app/model/phishing_model.pkl`

## 📊 Admin Dashboard  
View all previously analyzed URLs.

### Accessible at:

/dashboard

Displays:
- URL  
- Classification result  
- Timestamp  


## ☁ Deployment (Render)  
You can deploy using:

**Build Command:**

pip install -r requirements.txt

**Start Command:**

gunicorn app.app:app

## 👩‍💻 Author  
**Tanisha Mukharjee**  
AI & Software Development Enthusiast  
Mumbai, India  



## ⭐ Show Support  
If you like this project, don’t forget to ⭐ star the repository!


