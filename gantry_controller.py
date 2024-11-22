import time
from communication import Talker
from gantry import Gantry
from storage import FilamentHandler, FilamentSlot
from printer_spool import printerSpool

# Define custom exception
class ActionError(Exception):
    pass

def check_action(success, action_name):
    if not success:
        raise ActionError(f"Error: Expected \"{action_name}\" but action failed")

class Beast:
    def __init__(self, g_pico = 'COM7', s_pico = "COM11", p_pico = "COM10"):
        gantryPico = Talker(g_pico, timeout=1)
        storagePico = Talker(s_pico, timeout=1)
        printerPico = Talker(p_pico, timeout=1)

        self.gantryState = Gantry(gantryPico)
        self.storageState = FilamentHandler(storagePico)
        self.printerSpoolState = printerSpool(printerPico)

        self.activeSlot = FilamentSlot.ONE

    def home_state(self):
        home_state = False
        while not home_state:
            success = self.storageState.undock()
            check_action(success, 'undock()')
            success = self.printerSpoolState.undock()
            check_action(success, 'undock()')
            self.gantryState.docked = False
            success = self.gantryState.home()
            check_action(success, "home()")
            home_state = True

    def move_gantry_to(self, location):
        while True:
            success = self.gantryState.move_to(location)
            check_action(success, f"move_to({location})")
            if location == "storage_1":
                success = self.storageState.dock()
                check_action(success, "dock()")
                self.gantryState.position = "storage_1"
                self.gantryState.docked = True
                return
            elif location == "printer_1":
                success = self.printerSpoolState.dock()
                check_action(success, "dock()")
                self.gantryState.position = "printer_1"
                self.gantryState.docked = True
                return
            else:
                raise ActionError(f"Error: \"{location}\" not a valid location")

    def change_active_slot(self):
        self.storageState.change_slot(self.activeSlot)

    def load_gantry_with_filament(self, amount_secs = 60, speed = 1):
        # Deliver filament until intake is detected
        success = self.storageState.deliver_filament()
        check_action(success, "deliver_filament()")

        while not self.gantryState.check_intake():
            time.sleep(0.1)
        # Stop storage action
        success = self.storageState.stop()
        check_action(success, "stop()")

        success = self.storageState.extruder(80)
        check_action(success, "extruder(10)")

        success = self.gantryState.intake()
        check_action(success, "intake()")

        success = self.gantryState.spool(amount_secs, speed)
        check_action(success, "spool()")

        success = self.storageState.cut_filament()
        check_action(success, "cut_filament()")

        success = self.storageState.pull_out()
        check_action(success, "pull_out()")

        success = self.gantryState.retreiveFilament()
        check_action(success, "retreiveFilament()")

        success = self.storageState.undock()
        check_action(success, "undock()")
        if success:
            self.gantryState.docked = False


    def load_printer_with_filament(self):
        # Deliver filament until intake is detected
        success = self.gantryState.deliver_filament_until()
        check_action(success, "deliver_filament()")
        self.gantryState.talker.send_blind("Proceed")

        while not self.printerSpoolState.wait_for_intake():
            time.sleep(0.1)
            self.gantryState.talker.send_blind("Proceed")
        # Stop storage action
        success = self.gantryState.stop("Filament delivery stopped")
        check_action(success, "stop()")

        success = self.gantryState.deliver_filament(20)
        check_action(success, "deliver_filament()")

        success = self.printerSpoolState.intake_filament()
        check_action(success, "intake_filament()")

        success = self.gantryState.unspoolTension()
        check_action(success, "unspoolTension()")

        success = self.printerSpoolState.spool_up_until(1)
        check_action(success, "spool_up_until(1)")

        success = self.gantryState.unspoolTension(True)
        check_action(success, "unspoolTension(True)")
        # Stop storage action
        success = self.printerSpoolState.stop("Spool operation complete.")
        check_action(success, "stop()")