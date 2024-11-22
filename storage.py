from communication import Talker
import time

class FilamentSlot:
    ONE = "stepper_TL"
    TWO = "stepper_TR"
    THREE = "stepper_BL"
    FOUR = "stepper_BR"

class FilamentHandler:
    def __init__(self, talker: Talker):
        self.talker = talker
        self.state = "idle"
        self.active_slot = None

    def change_slot(self, slot):
        self.active_slot = slot
        print(f"Active slot changed to {self.active_slot}")
    

    def dock(self):
        try:
            command = "dock()"
            self.talker.send(command)
            print("Docking...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Dock successful.")
            if complete:
                print("Dock Successful")
                return True
            else:
                print("ERROR: Dock Unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def deliver_filament(self):
        try:
            command = f"{self.active_slot}.deliver_filament_until()"
            self.talker.send(command)
            print("Delivering filament...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivery started")
            if complete:
                print("Filament delivery started successfully")
                return True
            else:
                print("ERROR: Filament delivery not started")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def cut_filament(self):
        try:
            command = "cutFilament()"
            self.talker.send(command)
            print("Cutting filament...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament cutting successful.")
            if complete:
                print("Cutting filament successful")
                return True
            else:
                print("ERROR: Cutting filament unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def little_push(self):
        try:
            command = f"{self.active_slot}.little_push()"
            self.talker.send(command)
            print("Pushing filament slightly...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Little push successful.")
            if complete:
                print("Little push successful")
                return True
            else:
                print("ERROR: Little push unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False
    
    def pull_out(self):
        try:
            command = f"{self.active_slot}.pull_out()"
            self.talker.send(command)
            print("Pulling out...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Pull out successful.")
            if complete:
                print("Pull out successful")
                return True
            else:
                print("ERROR: Pull out unsuccessful.")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def extruder(self, amount):
        try:
            command = f"{self.active_slot}.deliver_filament({amount})"
            self.talker.send(command)
            print("Pushing filament slightly...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivery successful.")
            if complete:
                print("Extrusion successful")
                return True
            else:
                print("ERROR: extrusion unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def undock(self):
        try:
            command = "undock()"
            self.talker.send(command)
            print("Undocking...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Undock successful.")
            if complete:
                print("Undocking successful")
                return True
            else:
                print("ERROR: Undocking unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def stop(self):
        try:
            self.talker.send_blind("stop")
            print("Stopping...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivery stopped", 5)
            if complete:
                print("Delivery Stopped")
                return True
            self.talker.send("stop")
            print("Stopping...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivery stopped", 10)
            if complete:
                print("Delivery Stopped")
                return True
            self.talker.send("stop")
            print("Stopping...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivery stopped", 15)
            if complete:
                print("Delivery Stopped")
                return True
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def _wait_for_ack(self, success_message, timeout=30):
        start_time = time.time()
        partial_message = success_message[1:]  # Get message without first letter
        
        while True:
            reply = self.talker.receive()
            print(f"Received: {reply}")
            
            if reply == success_message or reply == partial_message:
                print(success_message)
                return True
                
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                print("Operation timed out.")
                return False