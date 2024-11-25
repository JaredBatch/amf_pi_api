from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gantry_controller import Beast

app = FastAPI()
beast = Beast()

class SlotChangeRequest(BaseModel):
    slot: int

class GantryMoveRequest(BaseModel):
    location: str

class FilamentLoadRequest(BaseModel):
    amount_secs: int = 60
    speed: int = 1

@app.post("/home")
def home():
    try:
        beast.home_state()
        return {"message": "Gantry homed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/move")
def move(request: GantryMoveRequest):
    try:
        beast.move_gantry_to(request.location)
        return {"message": f"Gantry moved to {request.location}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set-slot")
def set_slot(request: SlotChangeRequest):
    try:
        if 1 <= request.slot <= 4:
            beast.activeSlot = request.slot
            beast.change_active_slot()
            return {"message": f"Filament slot set to {request.slot}"}
        else:
            raise ValueError("Slot must be between 1 and 4")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/load-gantry")
def load_gantry(request: FilamentLoadRequest):
    try:
        beast.load_gantry_with_filament(request.amount_secs, request.speed)
        return {"message": "Gantry loaded with filament"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load-printer")
def load_printer():
    try:
        beast.load_printer_with_filament()
        return {"message": "Printer loaded with filament"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
