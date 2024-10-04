
import asyncio
import serial
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Define serial ports for each Pico (replace with correct device names)
PICO_PORTS = {
    "pico1": "/dev/ttyACM0",
    "pico2": "/dev/ttyACM1",
    "pico3": "/dev/ttyACM2"
}

# Store serial connections
serial_connections = {}

# Pydantic model for the JSON input
class JobData(BaseModel):
    material_slot: int
    printer_id: str

# Open serial connections to each Pico
def open_serial_connections():
    global serial_connections
    for pico, port in PICO_PORTS.items():
        serial_connections[pico] = serial.Serial(port, 9600, timeout=1)

# Function to send data to a specific Pico
async def send_to_pico(pico_name: str, message: str):
    if pico_name in serial_connections:
        ser = serial_connections[pico_name]
        ser.write(message.encode('utf-8'))
        # Optionally, wait for and process response
        await asyncio.sleep(0.1)  # Give time for the Pico to respond
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            return response
    return None

# Function to handle logic and send commands to all Picos
async def coordinate_actions(job_data: JobData):
    # Example action computation based on the JSON input and Pico states
    # Query each Pico and send necessary actions based on their state

    # Send actions to pico1
    response1 = await send_to_pico("pico1", f"Action for Pico 1 based on material slot {job_data.material_slot}\n")

    # Send actions to pico2
    response2 = await send_to_pico("pico2", f"Action for Pico 2 based on material slot {job_data.material_slot}\n")

    # Send actions to pico3
    response3 = await send_to_pico("pico3", f"Action for Pico 3 based on material slot {job_data.material_slot}\n")

    # You can perform additional logic based on the responses from the Picos
    print(f"Responses: {response1}, {response2}, {response3}")

    return {"status": "success", "pico_responses": [response1, response2, response3]}

# Endpoint to receive JSON requests and coordinate actions across Picos
@app.post("/receive-job")
async def receive_job(job_data: JobData):
    # Coordinate actions and send commands to Picos
    result = await coordinate_actions(job_data)
    return result

# Run when the server starts to establish serial connections
@app.on_event("startup")
async def startup_event():
    open_serial_connections()

# Run when the server shuts down to close serial connections
@app.on_event("shutdown")
async def shutdown_event():
    for ser in serial_connections.values():
        ser.close()
