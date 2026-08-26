# Real-Time Chat Application

A real-time chat application built using **Python, FastAPI, MySQL, HTML, CSS, JavaScript, and WebSocket**.

The application provides user registration, login authentication, and real-time messaging between connected users.

## 🚀 Features

* User Registration
* User Login
* Password Hashing
* MySQL Database
* FastAPI Backend
* WebSocket Real-Time Communication
* One-to-One Messaging
* Attractive Login Page
* Chat Interface
* Frontend served by FastAPI

## 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* SQLAlchemy
* PyMySQL
* Uvicorn
* WebSocket

### Frontend

* HTML
* CSS
* JavaScript

### Database

* MySQL

## 📁 Project Structure

```text
real-time-chat-application/
│
├── main.py
├── database.py
├── models.py
├── auth.py
├── .gitignore
│
└── frontend/
    ├── index.html
    ├── login.html
    ├── register.html
    └── chat.html
```

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/rohit23322/real-time-chat-application.git
```

### 2. Open the project

```bash
cd real-time-chat-application
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install required packages

```bash
pip install fastapi uvicorn sqlalchemy pymysql passlib
```

### 6. Configure MySQL

Create a MySQL database and update your `.env` file with your database connection details.

**Do not upload `.env` to GitHub.**

Example:

```text
DATABASE_URL=mysql+pymysql://username:password@localhost/database_name
```

### 7. Start the server

```bash
uvicorn main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## 🌐 Application Pages

| Page              | URL              |
| ----------------- | ---------------- |
| Home              | `/`              |
| Login             | `/login-page`    |
| Register          | `/register-page` |
| Chat              | `/chat-page`     |
| API Documentation | `/docs`          |

## 🔌 WebSocket

The application uses WebSocket for real-time communication.

WebSocket endpoint:

```text
/ws/{user_id}
```

Messages are sent in real time between connected users without refreshing the page.

## 🔐 Security

* Passwords are hashed before being stored.
* Database credentials are kept in `.env`.
* `.env` is excluded from Git using `.gitignore`.

## 📌 Future Improvements

* JWT authentication
* Online/offline user status
* Message history
* Group chat
* Message timestamps
* File and image sharing
* Read receipts
* User profile pictures
* Deployment to a cloud platform

## 👨‍💻 Author

**Rohit Khomane**

GitHub: https://github.com/rohit23322

## ⭐ Project

If you find this project useful, consider giving it a ⭐ on GitHub.
