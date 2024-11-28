# Gantry Control System

This repository contains the code for a control system that manages three subsystems using a gantry controller. Each subsystem is controlled by a Yukon microcontroller running MicroPython. The core component of this system is the `gantry_controller`, which manages the operation of multiple subsystems to achieve automated material handling for an additive manufacturing microfactory. This document provides an overview of each file and its role within the system, along with setup and usage instructions.

## Overview

The system is composed of the following main components:
- **Gantry Controller**: Coordinates the movement of the gantry system.
- **Storage Subsystem**: Manages filament storage and handling.
- **Printer Subsystem**: Loads filament into a 3D printer.
- **UI and API Interfaces**: Provides an API for controlling the system via a web UI and a touchscreen interface.

The core controller is a `Beast` class instance that interacts with each subsystem via serial communication. Each subsystem has a microcontroller responsible for performing specific actions (e.g., moving the gantry, docking/undocking, spooling filament).

## Components

### Files and Description

- **gantry_controller.py**
  - This script contains the main `Beast` class, which is the core controller managing the interactions between the gantry, storage, and printer subsystems.
  - Handles commands such as homing the gantry, moving to different positions, docking, undocking, and loading filament.

- **gantry.py**
  - Defines the `Gantry` class that represents the gantry's state and movements, including homing, moving, docking, and interacting with the filament.

- **storage.py**
  - Implements the `FilamentHandler` class, which controls the operations related to the filament storage subsystem, such as docking, delivering filament, cutting, and changing filament slots.

- **printer_spool.py**
  - Contains the `printerSpool` class, which manages the filament spool operations, including docking, undocking, spooling, and loading filament into the printer.

- **communication.py**
  - Defines the `Talker` class used to facilitate serial communication between the core system and the various microcontrollers.

- **pi_api_for_ui.py**
  - Provides a FastAPI-based REST API that allows for control of the gantry system via HTTP requests. This API includes endpoints for moving the gantry, loading filament, changing filament slots, and more.

- **pi_controller.py / AMF_GUI.py**
  - Provides a graphical user interface (GUI) using `ttkbootstrap` for controlling the gantry system via a touchscreen. Includes buttons for homing, moving to storage or printer, setting filament slots, and loading filament.

- **requirements.txt**
  - Lists the Python dependencies required to run the system, including `FastAPI`, `ttkbootstrap`, `pyserial`, and other packages.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.9+
- MicroPython installed on each Yukon microcontroller
- Required Python dependencies listed in `requirements.txt` (can be installed with `pip`)

### Installation

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd gantry-control-system
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Setup Microcontroller Communication**
   - Ensure the Yukon microcontrollers are connected to the correct serial ports as specified in the `Beast` class (`g_pico`, `s_pico`, `p_pico`).

### Running the System

1. **Run the FastAPI Server**
   ```
   uvicorn pi_api_for_ui:app --host 0.0.0.0 --port 8000
   ```
   This will start a web API that can be used to control the gantry via HTTP requests.

2. **Launch the GUI Application**
   Run either `pi_controller.py` or `AMF_GUI.py` to start the touchscreen GUI:
   ```
   python pi_controller.py
   ```

### API Endpoints

- **POST /home**: Homes the gantry to its initial position.
- **POST /move**: Moves the gantry to a specified location (`storage_1`, `printer_1`).
- **POST /set-slot**: Sets the active filament slot (1-4).
- **POST /load-gantry**: Loads the gantry with filament.
- **POST /load-printer**: Loads filament into the printer.

## System Flow

1. **Homing**: The system homes the gantry to ensure it starts from a known state.
2. **Moving**: The gantry moves between storage and printer positions as required.
3. **Loading Filament**: The system handles loading filament from storage to the gantry and subsequently into the printer.

## Troubleshooting

- **Serial Communication Issues**: Ensure that each microcontroller is properly connected and the serial port values (`g_pico`, `s_pico`, `p_pico`) are correct.
- **Unexpected Stops or Errors**: Refer to the error messages logged in the console. Ensure that each subsystem is correctly docked/undocked before issuing new commands.

## License

This project is licensed under the MIT License.

## Acknowledgements

This system leverages various technologies, including FastAPI, ttkbootstrap for the GUI, and MicroPython for the microcontrollers.

## Contact

For any questions or support, please contact [Your Contact Information].

