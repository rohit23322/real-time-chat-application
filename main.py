from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import engine, Base, SessionLocal
import models

from auth import hash_password, verify_password


# =========================================================
# APP
# =========================================================

app = FastAPI(title="Real-Time Chat Application Backend")


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FRONTEND
# =========================================================

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# =========================================================
# FRONTEND PAGES
# =========================================================

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/login-page")
def login_page():
    return FileResponse("frontend/login.html")


@app.get("/register-page")
def register_page():
    return FileResponse("frontend/register.html")


@app.get("/chat-page")
def chat_page():
    return FileResponse("frontend/chat.html")


# =========================================================
# REGISTER
# =========================================================

@app.post("/register")
def register(
    username: str,
    email: str,
    password: str
):

    db = SessionLocal()

    try:

        # Check email
        existing_email = db.query(models.User).filter(
            models.User.email == email
        ).first()

        if existing_email:

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Check username
        existing_username = db.query(models.User).filter(
            models.User.username == username
        ).first()

        if existing_username:

            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )

        # Hash password
        hashed_password = hash_password(password)

        # Create user
        new_user = models.User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

    finally:

        db.close()


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(
    email: str,
    password: str
):

    db = SessionLocal()

    try:

        # Find user
        user = db.query(models.User).filter(
            models.User.email == email
        ).first()

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(
            password,
            user.password
        ):

            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }

    finally:

        db.close()


# =========================================================
# CONNECTION MANAGER
# =========================================================

class ConnectionManager:

    def __init__(self):

        self.active_connections = {}


    async def connect(
        self,
        user_id: int,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections[user_id] = websocket

        print(
            f"User {user_id} connected"
        )


    def disconnect(
        self,
        user_id: int
    ):

        if user_id in self.active_connections:

            del self.active_connections[user_id]

            print(
                f"User {user_id} disconnected"
            )


    async def send_message(
        self,
        receiver_id: int,
        message: dict
    ):

        websocket = self.active_connections.get(
            receiver_id
        )

        if websocket:

            await websocket.send_json(
                message
            )


    async def broadcast(
        self,
        message: dict
    ):

        for websocket in self.active_connections.values():

            await websocket.send_json(
                message
            )


# Create manager
manager = ConnectionManager()


# =========================================================
# WEBSOCKET
# =========================================================

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int
):

    # Connect user
    await manager.connect(
        user_id,
        websocket
    )

    try:

        while True:

            # Receive message
            data = await websocket.receive_json()

            receiver_id = data.get(
                "receiver_id"
            )

            message_text = data.get(
                "message"
            )

            # Validate
            if not receiver_id:

                await websocket.send_json({
                    "error": "Receiver ID is required"
                })

                continue

            if not message_text:

                await websocket.send_json({
                    "error": "Message is required"
                })

                continue

            # Message object
            message_data = {

                "sender_id": user_id,

                "receiver_id": receiver_id,

                "message": message_text

            }

            print(
                "Message:",
                message_data
            )

            # Send to receiver
            await manager.send_message(
                receiver_id,
                message_data
            )

            # Send back to sender
            await manager.send_message(
                user_id,
                message_data
            )

    except WebSocketDisconnect:

        manager.disconnect(
            user_id
        )

    except Exception as e:

        print(
            "WebSocket error:",
            e
        )

        manager.disconnect(
            user_id
        )


# =========================================================
# SERVER TEST
# =========================================================

@app.get("/test")
def test():

    return {
        "message": "Chat Application Backend is working!"
    }