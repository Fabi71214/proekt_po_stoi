from fastapi import FastAPI, Request, Form,UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import sqlite3
import os

app = FastAPI(title="WB")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
os.makedirs("static/images", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    conn = sqlite3.connect("baza_tovar.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            Name TEXT ,
            new_price TEXT ,
            old_price TEXT,  
            rating TEXT ,
            data TEXT )
    ''')
    cursor.execute('SELECT * FROM Users')
    products = cursor.fetchall()
    conn.commit()
    count = len(products)
    conn.close()
    products = list(reversed(products))
    return templates.TemplateResponse("wb.html", {"request": request,
                                                  "products": products,
                                                  "count": count})
@app.post("/add_tovar")
def add_tovar(request:Request,
              image: UploadFile=File(None),
              title: str =Form(...),
              price: float =Form(...),
              old_price: float =Form(None),
              rating: float =Form(None),
              data: str =Form(None),
              ):
    conn = sqlite3.connect("baza_tovar.db")
    cursor = conn.cursor()
    content = image.file.read()
    f = open(f"static/images/{image.filename}", "wb")
    f.write(content)
    f.close()
    cursor.execute('''
        INSERT INTO Users (image, Name, old_price, new_price, rating, data)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (image.filename,
        title,
        str(old_price),                    
        str(price),                    
        str(rating),                 
        data                     
    ))
    conn.commit()
    conn.close()
if __name__ == "__main__":
    uvicorn.run(app, port=8989)