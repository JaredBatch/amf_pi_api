import time
from communication import Talker

class printerSpool:
    def __init__(self, talker: Talker):
        self.talker = talker

    def wait_for_intake(self, sensor="intake_sensor", timeout=0.1):
        try:
            command = f"check_intake()"
            self.talker.send(command)
            print(f"Waiting for {sensor} to be triggered...")
            complete = self._wait_for_ack("Sensor triggered", timeout)
            if complete:
                print(f"{sensor} triggered")
                return True
            else:
                print(f"ERROR: {sensor} not triggered within timeout")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def dock(self):
        try:
            command = "dock()"
            self.talker.send(command)
            print("Docking...")
            complete = self._wait_for_ack("Dock successful.", timeout=5)
            if complete:
                print("Dock successful")
                return True
            else:
                print("ERROR: Dock unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def undock(self):
        try:
            command = "undock()"
            self.talker.send(command)
            print("Undocking...")
            complete = self._wait_for_ack("Undock successful.", timeout=5)
            if complete:
                print("Undock successful")
                return True
            else:
                print("ERROR: Undock unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def spool_up(self, duration, max_speed):
        try:
            command = f"spool_up({duration}, {max_speed})"
            self.talker.send(command)
            print(f"Spooling up for {duration}s at max speed {max_speed}...")
            complete = self._wait_for_ack("Spool up complete.", timeout=duration + 25)
            if complete:
                print("Spool up complete")
                return True
            else:
                print("ERROR: Spool up incomplete or timed out")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False
        
    def spool_up_until(self, max_speed):
        try:
            command = f"spool_up_until({max_speed})"
            self.talker.send(command)
            print(f"Spooling up until stop trigger at max speed {max_speed}...")
            complete = self._wait_for_ack("RAMP UP", timeout=25)
            if complete:
                print("Spool up started")
                return True
            else:
                print("ERROR: Spool up didnt start")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False


    def intake_filament(self):
        try:
            command = "intake_filament()"
            self.talker.send(command)
            print("Intaking filament...")
            complete = self._wait_for_ack("Intake complete.", timeout=240)
            if complete:
                print("Intake complete")
                return True
            else:
                print("ERROR: Intake unsuccessful or timed out")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def stop(self):
        try:
            self.talker.send("STOP")
            print("Stopping...")
            time.sleep(0.1)
            complete = self._wait_for_ack("Operation stopped", timeout=5)
            if complete:
                print("Operation stopped")
                return True
            else:
                print("ERROR: Stop command unsuccessful")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    # Helper methods
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

    def _wait_for_response(self, timeout=30):
        start_time = time.time()
        response = ""
        while True:
            reply = self.talker.receive()
            if reply:
                response += reply
                # Assuming the response ends with a newline
                if "\n" in response:
                    return response.strip()
            if time.time() - start_time > timeout:
                print("Operation timed out.")
                return None