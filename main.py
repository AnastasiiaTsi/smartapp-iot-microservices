import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from controller.app_controller import AppController

app = FastAPI(title="SmartApp IoT System")

templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

controller = AppController()

@app.get("/")
async def root(request: Request):
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/toggle_speaker")
async def toggle_speaker(request: Request):
    controller.toggle_speaker()
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/toggle_light")
async def toggle_light(request: Request):
    controller.toggle_light()
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/toggle_curtains")
async def toggle_curtains(request: Request):
    controller.toggle_curtains()
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/set_volume")
async def set_volume(request: Request, volume: int = Form(...)):
    controller.set_speaker_volume(volume)
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/set_brightness")
async def set_brightness(request: Request, brightness: int = Form(...)):
    controller.set_light_brightness(brightness)
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/set_curtains_position")
async def set_curtains_position(request: Request, position: int = Form(...)):
    controller.set_curtains_position(position)
    devices = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

if __name__ == "__main__":
    print("🚀 Server starting at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)