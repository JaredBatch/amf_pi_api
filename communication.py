from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import serial
import time

class Talker:
    TERMINATOR = '\r'.encode('UTF8')

    def __init__(self, port, timeout=1):
        self.serial = serial.Serial(port, 115200, timeout=timeout)

    def send(self, text: str):
        # Ensure the text is formatted with carriage return
        line = '%s\r\f' % text
        self.serial.write(line.encode('utf-8'))
        reply = self.receive()
        reply = reply.replace('>>> ', '')  # Remove the REPL prompt      
        if reply != text:  # The line should be echoed
            #raise ValueError(f'Expected "{text}" got "{reply}"')
            print(f'Expected reply of"{text}" got "{reply}"')

    # def send(self, text: str):
    #     # Clear buffers before sending
    #     self.clear_buffer()
        
    #     # Ensure the text is formatted with carriage return and form feed
    #     line = '%s\r\f' % text
    #     self.serial.write(line.encode('utf-8'))
        
    #     while True:
    #         reply = self.receive()
    #         if reply == '>>>':
    #             reply = reply.replace('>>> ', '')
    #         else:
    #             print(f"Received unexpected message: {reply}")
    #             # Optionally, add a condition to prevent infinite loops
    #             continue  # Continue reading until we get the expected echo

    #     # No need for the previous equality check since we handle it in the loop

        
    def send_blind(self, text: str):
        # Ensure the text is formatted with carriage return and form feed
        line = '%s\r\f' % text
        self.serial.write(line.encode('utf-8'))

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def close(self):
        self.serial.close()

    def clear_buffer(self):
        """Clears the serial input and output buffers."""
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        # Read and discard any data in the input buffer
        while self.serial.in_waiting:
            self.serial.read(self.serial.in_waiting)



