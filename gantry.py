from communication import Talker
import time

class GantryState:
    WAIT = "wait"
    MOVING = "moving"
    INTAKE = "intake"
    SPOOLING = "spooling"
    DELIVER = "deliver"
    UNSPOOL = "unspool"
    ERROR = "error"

class GantryPosition:
    UNKNOWN = "unknown"
    HOME = "home"
    STORAGE_1 = "storage_1"
    #STORAGE_2 = "storage_2"
    PRINTER_1 = "printer_1"

    @staticmethod
    def order():
        return [
            GantryPosition.HOME,
            GantryPosition.STORAGE_1,
            #GantryPosition.STORAGE_2,
            GantryPosition.PRINTER_1,
        ]

class Gantry:
    def __init__(self, talker: Talker):
        self.position = GantryPosition.UNKNOWN
        self.docked = False
        self.state = GantryState.WAIT
        self.talker = talker

    def home(self):
        if self.docked:
            print("Cannot move while docked.")
            self.state = GantryState.ERROR
            return False
        
        self.state = GantryState.MOVING
        try:
            command = "home()"
            self.talker.send(command)
            print("Moving to home...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Home Success")
            if complete:
                self.position = GantryPosition.HOME
                self.state = GantryState.WAIT
                print("Homing successful.")
                return True
            else:
                print("ERROR: Homing Failed")
                self.state = GantryState.ERROR
                return False
        except ValueError as e:
            print(f"Error: {e}")
            self.state = GantryState.ERROR
            return False

    def move_to(self, target_position):
        if self.position == GantryPosition.UNKNOWN:
            print("Current position unknown. Moving to home first.")
            if not self.home():
                return False

        if self.docked:
            print("Cannot move while docked.")
            self.state = GantryState.ERROR
            return False
        
        positions = GantryPosition.order()
        
        if target_position not in positions:
            print(f"Invalid target position: {target_position}")
            self.state = GantryState.ERROR
            return False

        current_index = positions.index(self.position)
        target_index = positions.index(target_position)

        if current_index < target_index:
            steps = target_index - current_index
            command = f"move_left({steps})"
        elif current_index > target_index:
            steps = current_index - target_index
            command = f"move_right({steps})"
        else:
            print("Already at the target position.")
            return True

        self.state = GantryState.MOVING
        try:
            self.talker.send(command)
            print(f"Moving {steps} step(s) {'left' if current_index < target_index else 'right'} to {target_position}...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Movement Successful")
            if complete:
                self.position = target_position
                self.state = GantryState.WAIT
                print("Movement successful.")
                return True
            else:
                print("ERROR: Movement Failed")
                self.state = GantryState.ERROR
                return False
        except ValueError as e:
            print(f"Error: {e}")
            self.state = GantryState.ERROR
            return False

    def dock(self):
        if self.position in [GantryPosition.STORAGE_1, GantryPosition.PRINTER_1]:
            try:
                command = "dock()"
                self.talker.send(command)
                print("Docking...")
                time.sleep(0.1)
                complete = self._wait_for_ack("Dock successful.")
                if complete:
                    self.docked = True
                    print("Dock Successful")
                    return True
                else:
                    print("ERROR: Dock Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print("Cannot dock here.")
            self.state = GantryState.ERROR
            return False

    def undock(self):
        try:
            command = "undock()"
            self.talker.send(command)
            print("Undocking...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Undock successful.")
            if complete:
                self.docked = False
                print("Undock Successful")
                return True
            else:
                print("ERROR: Undock Unsuccessful")
                self.state = GantryState.ERROR
                return False
        except ValueError as e:
            print(f"Error: {e}")
            self.state = GantryState.ERROR
            return False

    def check_intake(self):
        try:
            command = 'check_intake()'
            self.talker.send(command)
            print("Checking intake...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Locked and Loaded", 0.1)
            if complete:
                print("Intake check successful.")
                return True
            else:
                return False
        except ValueError as e:
            print(f"Error: {e}")
            self.state = GantryState.ERROR
            return False

    def intake(self):
        if self.docked and self.position == GantryPosition.STORAGE_1:
            try:
                command = "intake_filament()"
                self.talker.send(command)
                print("Intaking material...")
                time.sleep(0.1)
                complete = self._wait_for_ack("Intake successful.", 360)
                if complete:
                    print("Intake Successful")
                    self.state = GantryState.INTAKE
                    return True
                else:
                    print("ERROR: Intake Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print(self.docked)
            print(self.position)
            print("Intake failed.")
            self.state = GantryState.ERROR
            return False

    def spool_until(self, speed):
        if self.state == GantryState.INTAKE:
            try:
                command = f"spool_up_until({speed})"
                self.talker.send(command)
                print("Spooling material...")
                time.sleep(0.1)
                complete = self._wait_for_ack("**Full Speed Phase**")
                if complete:
                    print("Spooling")
                    self.state = GantryState.SPOOLING
                    return True
                else:
                    print("ERROR: Spool Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print("Cannot spool without intaking.")
            self.state = GantryState.ERROR
            return False
        
    def spool(self, spool_time, speed):
        if self.state == GantryState.INTAKE:
            try:
                command = f"spool_up({spool_time}, {speed})"
                self.talker.send(command)
                print("Spooling material...")
                time.sleep(0.1)
                complete = self._wait_for_ack("Spool successful.", 360)
                if complete:
                    print("Spool Successful")
                    self.state = GantryState.SPOOLING
                    return True
                else:
                    print("ERROR: Spool Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print("Cannot spool without intaking.")
            self.state = GantryState.ERROR
            return False
    
    def deliver_filament_until(self):
        try:
            command = "deliverFilamentUntil()"
            self.talker.send(command)
            print("Delivering filament...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivery started")
            if complete:
                self.state = GantryState.DELIVER
                print("Filament delivery started successfully")
                return True
            else:
                print("ERROR: Filament delivery not started")
                self.state = GantryState.ERROR
                return False
        except ValueError as e:
            self.state = GantryState.ERROR
            print(f"Error: {e}")
            return False
        
    def deliver_filament(self, length):
        try:
            command = f"deliverFilament({length})"
            self.talker.send(command)
            print("Delivering {length}mm of filament...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Filament delivered successfully.")
            if complete:
                self.state = GantryState.DELIVER
                print("Filament delivery started successfully")
                return True
            else:
                print("ERROR: Filament delivery not started")
                self.state = GantryState.ERROR
                return False
        except ValueError as e:
            print(f"Error: {e}")
            self.state = GantryState.ERROR
            return False
        

    def retreiveFilament(self):
        if self.state == GantryState.SPOOLING:
            try:
                command = "retreiveFilament()"
                self.talker.send(command)
                print("Retreiving filament...")
                time.sleep(0.1)
                complete = self._wait_for_ack("Filament retrieved.", 240)
                if complete:
                    print("Retrieve Successful")
                    return True
                else:
                    print("ERROR: Retrieve Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print("Cannot retrieve without spooling")
            self.state = GantryState.ERROR
            return False

    def unspool(self):
        if self.state == GantryState.DELIVER:
            try:
                command = "unspool()"
                self.talker.send(command)
                print("Unspooling material...")
                time.sleep(0.1)
                complete = self._wait_for_ack("Unspool successful.")
                if complete:
                    self.state = GantryState.UNSPOOL
                    print("Unspool Successful")
                    return True
                else:
                    print("ERROR: Unspool Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print("Cannot unspool without delivering.")
            self.state = GantryState.ERROR
            return False
        
    def unspoolTension(self, interrupt = False):
        if self.state == GantryState.DELIVER:
            try:
                command = "unspoolTension()"
                self.talker.send(command)
                print("Revieving motor tension material...")
                if not interrupt:
                    time.sleep(0.1)
                    complete = self._wait_for_ack("Tension off.")
                    if complete:
                        print("Tension off Successful")
                else:
                    time.sleep(0.1)
                    complete = self._wait_for_ack("Filament off spool.", 3000)
                    if complete:
                        self.state = GantryState.UNSPOOL
                        print("Spool off")
                if complete:
                    return True
                else:
                    print("ERROR: Tension off Unsuccessful")
                    self.state = GantryState.ERROR
                    return False
            except ValueError as e:
                print(f"Error: {e}")
                self.state = GantryState.ERROR
                return False
        else:
            print("Cannot unspool tension without delivering.")
            self.state = GantryState.ERROR
            return False
        
    def stop(self, success_message):
        try:
            self.talker.send_blind("STOP")
            print("Stopping...")
            time.sleep(0.1)
            complete = self._wait_for_ack(f"{success_message}", 5)
            if complete:
                print("Delivery Stopped")
                return True
            self.talker.send("STOP")
            time.sleep(0.1)
            print("Stopping...")
            complete = self._wait_for_ack(f"{success_message}", 10)
            if complete:
                print("Delivery Stopped")
                return True
            self.talker.send("STOP")
            time.sleep(0.1)
            print("Stopping...")
            complete = self._wait_for_ack(f"{success_message}", 15)
            if complete:
                print("Action Stopped")
                return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
        
    def wait_for_input(self, message, timeout=30):
        start_time = time.time()
        while True:
            reply = self.talker.receive()
            print(f"Received: {reply}")
            if reply == message:
                print(message)
                return True

            if time.time() - start_time > timeout:
                print(f"{message} not received before timeout of {timeout}")
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
