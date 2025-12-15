# 🏥 Patient Management System API

A **FastAPI-based REST API** to manage patient records with features like **BMI calculation, health verdicts, sorting, and CRUD operations**, all backed by a simple JSON data store.

This project is ideal for **learning FastAPI, Pydantic models, validation, and REST API design**.

---

## 🚀 Features

* Create, read, update, and delete patient records
* Automatic **BMI calculation**
* Health **verdict generation** (Underweight, Normal, Overweight, Obese)
* Sort patients by **height, weight, or BMI**
* Input validation using **Pydantic**
* Interactive API docs via **Swagger UI**
* Lightweight JSON-based storage (no database required)

---

## 🛠 Tech Stack

* **Python 3.9+**
* **FastAPI**
* **Pydantic**
* **Uvicorn**
* **JSON** (file-based storage)

---

## 📁 Project Structure

```
.
├── main.py               # FastAPI application
├── patients.json         # Data storage file
├── README.md             # Project documentation
└── requirements.txt      # Project dependencies
```

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Prakashbishal/FastAPI.git
cd patient-management-api
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows
```

### 3️⃣ Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI provides built-in interactive docs:

* **Swagger UI:**
  👉 `http://127.0.0.1:8000/docs`

* **ReDoc:**
  👉 `http://127.0.0.1:8000/redoc`

---

## 🔗 API Endpoints

### 🔹 Basic

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| GET    | `/`      | API welcome message |
| GET    | `/about` | API description     |

---

### 🔹 Patient Operations

| Method | Endpoint                 | Description            |
| ------ | ------------------------ | ---------------------- |
| GET    | `/view`                  | View all patients      |
| GET    | `/patients/{patient_id}` | View patient by ID     |
| POST   | `/create`                | Create a new patient   |
| PUT    | `/edit/{patient_id}`     | Update patient details |
| DELETE | `/delete/{patient_id}`   | Delete a patient       |

---

### 🔹 Sorting

| Method | Endpoint | Description                             |
| ------ | -------- | --------------------------------------- |
| GET    | `/sort`  | Sort patients by height, weight, or BMI |

**Query Parameters**

```text
sort_by = height | weight | bmi
order   = asc | desc
```

Example:

```
/sort?sort_by=bmi&order=desc
```

---

## 🧾 Sample Patient JSON

```json
{
  "id": "P001",
  "name": "John Doe",
  "city": "London",
  "age": 28,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
```

---

## 🧮 BMI Logic

```
BMI = weight (kg) / height² (m²)
```

| BMI Range   | Verdict     |
| ----------- | ----------- |
| < 18.5      | Underweight |
| 18.5 – 24.9 | Normal      |
| 25 – 29.9   | Overweight  |
| ≥ 30        | Obese       |

---

## ⚠️ Notes

* `patients.json` must exist before running the app.
* This project uses **file-based storage**, not suitable for production.
* For real applications, replace JSON with **SQLite/PostgreSQL**.

---

## 🔮 Future Improvements

* Authentication & authorization
* Database integration
* Pagination & filtering
* Logging & error tracking
* Deployment with Docker

---

## 🤝 Contributing

Contributions are welcome.
Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is for **educational purposes**.

---

