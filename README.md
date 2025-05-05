# 💼 Salary Prediction App

A full-stack machine learning application that predicts employee salaries using both **regression** and **classification** models.

---

## 🚀 Features

- Predict salary as a numeric value (regression) or Classify salary into ranges such as Low / Mid / High (classification)
- User-friendly web interface for input and results
- Fast and scalable API using FastAPI

---

## 🧠 Tech Stack

### 📊 Machine Learning
- Regression & Classification models (e.g., Random Forest, XGBoost)
- Encoders and data preprocessing pipelines

### 👥 Backend
- FastAPI for serving predictions
- Pydantic for input validation
- Model loading with joblib or pickle

### 🌐 Frontend
- HTML, CSS, and JavaScript (can be extended with modern frameworks)
- Interactive UI with dropdowns and styled forms

---

## 📁 Project Structure

```
├── models/                  # Trained ML models
├── app/                    # FastAPI backend
│   └── main.py             # API logic
├── frontend/               # Static frontend files
│   └── index.html          # Main HTML form
├── requirements.txt        # Dependencies
└── README.md               # Project description
```