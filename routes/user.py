from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User

from cryptography.fernet import Fernet

user = APIRouter()
key = Fernet.generate_.key()
f = Fernet(key)


@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()


@user.get("/users/{id}")
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.post("/")
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.put("/{id}")
def update_user(user: User, id: int):
    conn.execute(
        users.update()
        .values(name=user.name, email=user.email, password=user.password)
        .where(users.c.id == id)
    )
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete("/{id}")
def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
