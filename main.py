from fastapi import FastAPI,Form,Request,Depends
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from os import getenv
from fastapi.staticfiles import StaticFiles

from database import engine,get_db
from models import base,User
from security import verify_password,hash_password

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
base.metadata.create_all(engine)
templates=Jinja2Templates(directory="templates")
app.add_middleware(
    SessionMiddleware,
    secret_key=getenv("secret_key"),
    https_only=False,
    same_site="lax",
    max_age=60*60*24*30
)
@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    user_id=request.session.get("user_id")
    return templates.TemplateResponse(
        request,"home.html",{"user_id":user_id}
    )
@app.get("/register",response_class=HTMLResponse)
def register(request:Request):
    return templates.TemplateResponse(request,"register.html")
@app.post("/register") 
def register(
    request:Request,
    name:str =Form(),
    email:str =Form(),
    password:str =Form(),
    db:Session=Depends(get_db) 
) :
    errors=[]
    if not name.strip():
        errors.append("Name is required.")
    if not email.strip():
        errors.append("Email is required.")  
    if len(password)<8:
        errors.append("Password must be at least 8 characters long.") 
    existing_user=db.query(User).filter(User.email==email).first()
    if existing_user:
        errors.append("An account with this email already exists")
    if errors:
        return templates.TemplateResponse(request,"register.html",{"errors":errors})   
    
    new_user=User(
        name=name.strip(),
        email=email.strip(),
        password_hash=hash_password(password),
        role="student",)
    db.add(new_user)
    db.commit()
    return RedirectResponse("/login",status_code=303)   
@app.get("/login",response_class=HTMLResponse)  
def login(request:Request):
    return templates.TemplateResponse(request,"login.html")

@app.post("/login")
def login(
    request:Request,
    email:str=Form(),
    password:str=Form(),
    db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==email).first()
    if not user or not verify_password(password,user.password_hash):
        return templates.TemplateResponse(request,"login.html",{"error":"Invalid email or password."})
    request.session["user_id"]=user.id
    return RedirectResponse("/dashboard",status_code=303)
@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request,db:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login",status_code=303)
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        request.session.clear()
        return RedirectResponse("/login",status_code=303)
    return templates.TemplateResponse(request,"dashboard.html",{"user":user})    

@app.get("/admin",response_class=HTMLResponse)
def admin(request:Request,db:Session=Depends(get_db)):
    user_id=request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login",status_code=303)
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        request.session.clear()
        return RedirectResponse("/login",status_code=303)

    if user.role != "admin":
        return templates.TemplateResponse(request,"access_denied.html",status_code=403)
    all_users=db.query(User).all()
    return templates.TemplateResponse(request,"admin.html",{"user":user,"all_users":all_users})    


@app.get("/logout")
def logout(request:Request):
    request.session.clear()
    return RedirectResponse("/",status_code=303)
