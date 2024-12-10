from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

# Инициализация приложения и шаблонов
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Список пользователей
users: List[User] = [
    User(id=1, username="UrbanUser", age=24),
    User(id=2, username="UrbanTest", age=22),
    User(id=3, username="Capybara", age=60),
]

# Маршрут для отображения списка пользователей
@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Маршрут для отображения информации о пользователе
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return templates.TemplateResponse("users.html", {"request": request, "users": [], "error": "Пользователь не найден"})
    return templates.TemplateResponse("users.html", {"request": request, "user": user})
