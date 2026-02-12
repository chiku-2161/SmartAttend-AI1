# SmartAttend AI  
### Intelligent Face-Based Attendance & Risk Analytics System

---

## 📌 Overview

**SmartAttend AI** is an end-to-end intelligent attendance system that uses:

- **Face Recognition**
- **Real-time presence tracking**
- **Automated attendance classification**
- **Risk analytics dashboard**

to eliminate **proxy attendance**, reduce **manual effort**, and provide **data-driven academic insights**.

---

## 🚀 Key Features

- 🎥 Real-time **face recognition attendance**
- ⏱️ **Continuous presence tracking** during class
- 📊 Automatic classification:
  - **Present**
  - **Late**
  - **Absent**
- 🧠 **Risk analytics engine**
  - High → Absent  
  - Medium → Late  
  - Low → Present
- 📈 **Dashboard analytics**
- 🔮 **Attendance forecasting**
- 🧾 **CSV export of final attendance**
- 🧪 Debug APIs for **live verification**

---

## 🏗️ System Architecture

### 1. AI Recognition Layer
- OpenCV-based face detection & recognition  
- Returns **student ID** for attendance marking  

### 2. Backend Attendance Engine
- **Flask REST API**
- **SQLite database**
- Session-based attendance tracking
- Risk & analytics computation

### 3. Teacher Control Panel (CLI)

Flow:

```
Start Class → Scan Faces → End Class → View Dashboard
```

---

## 🔄 Workflow

1. **Teacher starts class**
   - Session created in database  

2. **Face scanning**
   - Presence score increases per detection  

3. **Class ends**
   - Attendance % calculated  
   - Status assigned (Present/Late/Absent)  
   - Risk analytics generated  
   - CSV exported  

4. **Dashboard**
   - Shows attendance distribution  
   - Displays risk levels  

---

## 🧪 Technologies Used

### AI / Computer Vision
- OpenCV  
- Face Recognition (LBPH / embeddings)

### Backend
- Python  
- Flask REST API  
- SQLite  

### System Design
- Session-based tracking  
- Presence scoring algorithm  
- Risk analytics engine  

---

## 📊 Risk Logic

| Attendance Status | Risk Level |
|-------------------|-----------|
| Absent | High |
| Late | Medium |
| Present | Low |

---

## ▶️ How to Run

### 1️⃣ Start Backend Server

```bash
python -m smart_attendance_system.app
```

Server runs at:

```
http://127.0.0.1:5000
```

---

### 2️⃣ Run Teacher Panel

```bash
python main.py
```

Menu:

```
1. Register Face
2. Start Class
3. Scan Attendance
4. End Class
5. Exit
```

---

### 3️⃣ View Final Attendance (Debug)

Open in browser:

```
http://127.0.0.1:5000/debug/attendance/<session_id>
```

Replace `<session_id>` with the actual session number.

---

## 📁 Project Structure

```
smart_attendance_system/
│
├── app.py
├── database.py
├── routes/
│   ├── attendance_routes.py
│   ├── analytics_routes.py
│   ├── teacher_routes.py
│   └── student_routes.py
│
├── services/
│   ├── risk_engine.py
│   ├── forecast_engine.py
│   └── analytics_service.py
│
main.py
dev2_demo.py
attendance.db
```

---

## 🌟 Impact

### For Teachers
- Saves lecture time  
- Detects low-attendance students early  
- Provides instant analytics  

### For Institutions
- Eliminates proxy attendance  
- Enables data-driven monitoring  
- Scalable toward **Smart Campus systems**  

---

## 🔮 Future Scope

- Web dashboard UI  
- Cloud deployment  
- Multi-camera classrooms  
- Mobile teacher app  
- AI behavioral analytics  

---

## 🏁 Conclusion

**SmartAttend AI** is more than an attendance tool.  
It is a **complete intelligent academic monitoring platform** combining:

- Artificial Intelligence  
- Real-time analytics  
- Automated risk detection  

to create a **proxy-free, insight-driven classroom environment**.

---

### 👨‍💻 Developed for AI/ML Hackathon  
**SmartAttend AI — Turning classrooms into intelligent learning spaces.**
