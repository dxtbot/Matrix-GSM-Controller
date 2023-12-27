import time
import os
import serial
import threading
import re

# Define the ASCII art
ascii_art = """
  ______  _______    ____ ____  __  __   _____ ___   ___  _     
 |  _ \ \/ /_   _|  / ___/ ___||  \/  | |_   _/ _ \ / _ \| |    
 | | | \  /  | |   | |  _\___ \| |\/| |   | || | | | | | | |    
 | |_| /  \  | |   | |_| |___) | |  | |   | || |_| | |_| | |___ 
 |____/_/\_\ |_|    \____|____/|_|  |_|   |_| \___/ \___/|_____|       
"""

ascii_art1 = """
        ||
  ______||
 / ____ o|
| / ;; \ |
| ______ |
||______||
||  D2  ||
||______||
|'\[--]/'|
|  ¨''¨  |
|  ''''  |
|        |
|        |
|        |
|________|
"""

ascii_art2 = """
____¶¶¶¶_______________________________¶¶¶¶
__¶¶¶11¶¶¶___________________________¶¶¶11¶¶¶
_¶¶111111¶¶_________________________¶¶111111¶¶
_¶¶111111¶¶_________________________¶¶111111¶¶
__¶¶¶111¶¶___________________________¶¶1111¶¶
____¶¶¶11¶¶__________________________¶¶11¶¶¶
______¶¶11¶¶_______¶¶¶¶¶¶¶¶¶________¶¶11¶¶
_______¶¶11¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11¶¶
________¶¶11¶¶11111111111111111111¶¶11¶¶
______¶¶¶11111111111111111111111111111¶¶¶
____¶¶¶1111111111111111111111111111111111¶¶
___¶¶11111111111111111111111111111111111111¶¶
__¶11111111111111111111111111111111111111111¶¶
_¶1111111111111111111111111111111111111111111¶¶
¶¶1111111111111111111111111111111111111111111¶¶
¶¶11111111111111111111111111111111111111111111¶
_¶11111111111¶¶¶¶¶11111111111¶¶¶¶¶11111111111¶¶
_¶¶11111111111111111111111111111111111111111¶¶
__¶¶¶11111111¶¶¶¶¶¶¶¶1111111¶¶¶¶¶¶¶¶1111111¶¶
____¶¶11111¶¶¶¶¶¶¶_¶¶¶1111¶¶¶¶¶¶¶__¶¶1111¶¶¶
_____¶¶111¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶___¶¶11¶¶
_______¶11¶¶¶¶¶¶¶¶¶_¶¶¶11¶¶¶¶¶¶¶¶¶_¶¶¶1¶¶
______¶¶111¶¶¶¶¶¶¶¶¶¶¶1111¶¶¶¶¶¶¶¶¶¶¶111¶
_____¶¶11111¶¶¶¶¶¶¶¶11111111¶¶¶¶¶¶¶111111¶
_____¶1111111111111111¶¶1¶111111111111111¶
_____¶¶111111111111111¶111¶1111111111111¶¶
______¶¶1111111111111111111111111111111¶¶
_______¶¶11111111111111111111111111111¶¶
_________¶¶¶11111111¶¶¶¶¶¶¶¶¶1111111¶¶¶
___________¶¶¶¶1111111¶¶¶¶¶11111¶¶¶¶
______________¶¶¶¶1111111111111¶¶¶
_________________¶¶11111111111¶¶
__________________¶¶¶¶¶¶¶¶¶¶¶¶¶

"""

def extract_word_in_quotes(response):
    match = re.search(r'"([^"]*)"', response)
    if match:
        return match.group(1)
    else:
        return None

def send_command(serial_port, command):#expected_response="OK"
    serial_port.write((command + '\r\n').encode())
    time.sleep(2)
    return serial_port.read_all().decode()


def send_command1(serial_port, command, expected_response="OK"):
    serial_port.write((command + '\n').encode())
    time.sleep(1)
    response = serial_port.read_all().decode()

    if expected_response in response:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
        print(ascii_art)  # Display ASCII art
        return response
    else:
        return "Nothing found"

def check_imei(serial_port):
    imei_command = 'AT+GSN'
    response = send_command(serial_port, imei_command)

    if "ERROR" in response:
        print("Failed to retrieve IMEI.")
    else:
        imei = response.strip()
        print("IMEI:", imei)


def signal_report(serial_port):
    signal_command = 'AT+CSQ'
    response = send_command(serial_port, signal_command)

    if "ERROR" in response:
        print("Failed to retrieve signal report.")
    else:
        signal_values = response.strip().split(':')[1].split(',')[0]
        signal_strength = int(signal_values) if signal_values.isdigit() else None
        integer_value = int(signal_values)
        if integer_value is not None:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
            print(ascii_art)  # Display ASCII art
            scaled_signal = (integer_value / 31) * 100
            formatted_scaled_signal = "{:.1f}".format(scaled_signal)
            print("Signal Quality:", formatted_scaled_signal, "%")
        else:
            print("Unable to calculate scaled signal.")


def insert_pin(serial_port):
    pin = input("Enter the 4-digit PIN code: ")
    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN. Please enter a 4-digit numerical PIN.")
        return

    pin_command = f'AT+CPIN="{pin}"'
    response = send_command(serial_port, pin_command)

    if "OK" in response:
        print("PIN successfully set.")
    else:
        print("Failed to set PIN. Please check the provided PIN or module settings.")

def make_phone_call(serial_port):
    # Functionality to make a phone call
    phone_number = input("Enter the phone number to make a call: ")
    send_command(serial_port, f'ATD{phone_number};')  # Dial the phone number
    print(f"Calling {phone_number}...")

    time.sleep(10)  # Call duration
    send_command(serial_port, "ATH")  # Hang up the call
    print("Call ended.")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
    print(ascii_art)  # Display ASCII art

#def read_messages(serial_port):
 #   os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
 #   print(ascii_art)  # Display ASCII art
 #   messages = send_command(serial_port, 'AT')
 #   messages = send_command(serial_port, 'AT+CMGL="ALL"')
 #   print("Received Messages:")
 #   print(messages)

def read_messages(serial_port):
    response = send_command(serial_port, 'AT+CMGL="ALL"')
    print("Full Response:")
    print(response)
    print("Decoded SMS Information:")

def send_sms(serial_port):
    # Functionality to send SMS
    phone_number = input("Enter the phone number to send SMS: ")
    message = input("Enter the message: ")

    send_command(serial_port, 'AT+CMGF=1')  # Set SMS text mode
    send_command(serial_port, f'AT+CMGS="{phone_number}"')  # Send SMS command

    send_command(serial_port, message + chr(26))  # Enter the message and CTRL+Z to send
    print("SMS sent successfully!")
    time.sleep(2)  # Delay of 2 seconds
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
    print(ascii_art)  # Display ASCII art

# New function for picking up the phone (Option 7)
def pick_up_phone(serial_port):
    send_command(serial_port, "ATA")  # Answer the call
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
    print(ascii_art)  # Display ASCII art
    print("Picking up the phone...")
    time.sleep(2)
    return


# New function for hanging up the phone (Option 8)
def hang_up_phone(serial_port):
    send_command(serial_port, "ATH")  # Hang up the call
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
    print(ascii_art)  # Display ASCII art
    print("Hanging up the phone...")
    time.sleep(2)
    return

# Functionality to send SMS to numbers from a file with a delay of 5 seconds
def send_sms_from_file(serial_port):
    # Functionality to send SMS to numbers from a file
    filename = 'SMSBOMB.txt'
    try:
        with open(filename, 'r') as file:
            message = input("Enter the message to send: ")
            send_command(serial_port, 'AT+CMGF=1')  # Set SMS text mode
            for line in file:
                data = line.strip().split(',')
                if len(data) == 2:
                    name, phone_number = data[0].strip(), data[1].strip()
                    # Extract the phone number without 'nr = ' and ')'
                    phone_number = phone_number.replace('nr = ', '').replace(')', '')
                    phone_number = phone_number.replace('"', '')  # Remove any remaining double quotes
                    send_command(serial_port, 'AT+CMGF=1')  # Set SMS text mode
                    send_command(serial_port, f'AT+CMGS="{phone_number}"')  # Send SMS command
                    send_command(serial_port, message + chr(26))  # Enter the message and CTRL+Z to send
                    print(f"SMS sent to {name} ({phone_number})")
                    time.sleep(1)  # Delay of 2 seconds
    except FileNotFoundError:
        print(f"Error: {filename} not found")
    time.sleep(1)  # Delay of 5 seconds before clearing the screen
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen after the operation
    print(ascii_art)  # Display ASCII art

# Function to display ICCID (Option 5)
def display_iccid(serial_port):
    # Functionality to display ICCID
    response = send_command1(serial_port, "AT+CCID")
    print("")
    print(response)

# Function to display Product Identification Information (Option 6)
def display_product_info(serial_port):
    # Functionality to display product identification information
    response = send_command1(serial_port, "ATI")
    print("")
    print(response)

# Function to handle incoming calls
def answer_or_reject_call(serial_port, caller_id):
    print(ascii_art1)  # Display ASCII art
    print(f"Incoming call detected from {caller_id} for pickup select 5 !")
    return


check_calls_flag = True  # Global flag to control checking for incoming calls

def check_incoming_calls(serial_port):
    global check_calls_flag
    while check_calls_flag:
        if serial_port.in_waiting > 0:
            incoming_data = serial_port.readline().decode().strip()
            if "+CLIP:" in incoming_data:
                caller_id = incoming_data.split('"')[1]  # Extracts the phone number within double quotes
                answer_or_reject_call(serial_port, caller_id)
        else:
            time.sleep(0.1)  # Add a small delay to avoid continuous checking and give CPU time to other operations

def temporary_disable_calls_check():
    global check_calls_flag
    check_calls_flag = False
    time.sleep(10)  # Wait for 10 seconds (adjust as needed)
    check_calls_flag = True  # Enable checking for incoming calls afte

# Main function
def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before displaying options
    print(ascii_art2)  # Display ASCII art
    com_port = input("Enter COM port (e.g., COM1): ")

    try:
        ser = serial.Serial(com_port, 9600, timeout=1)
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before displaying options
        print(ascii_art)  # Display ASCII art
        print(f"Connected to {com_port}")

        response = send_command(ser, "AT")
        if "OK" in response:
            print("GSM module is working properly")
            response = send_command(ser, "AT+COPS?")
            extracted_word = extract_word_in_quotes(response)
            if extracted_word:
                print(f"Connected to provider: {extracted_word}")
            else:
                print("No word found between quotes.")

            time.sleep(3)  # Delay 3 seconds

            call_thread = threading.Thread(target=check_incoming_calls, args=(ser,), daemon=True)
            call_thread.start()

            while True:
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before displaying options
                print(ascii_art)  # Display ASCII art
                print("Choose an option:")
                print("1: Make Phone Call")
                print("2: Send SMS")
                print("3: Read SMS")
                print("4: Send SMS to All from File")
                print("5: Show ICCID")
                print("6: Display Product Identification Information")
                print("7: Pick up the phone")
                print("8: Hang up the phone")
                print("9: Reject Incoming Call")
                print("10: Insert PIN ****")
                print("11: Check IMEI")
                print("12: Check Signal")
                print("13: Exit")

                option = input("Enter your choice: ")

                if option == '1':
                    make_phone_call(ser)
                elif option == '2':
                    send_sms(ser)
                elif option == '3':
                    threading.Thread(target=temporary_disable_calls_check).start()
                    read_messages(ser)
                elif option == '4':
                    send_sms_from_file(ser)
                elif option == '5':
                    threading.Thread(target=temporary_disable_calls_check).start()
                    display_iccid(ser)
                elif option == '6':
                    threading.Thread(target=temporary_disable_calls_check).start()
                    display_product_info(ser)
                elif option == '7':
                    pick_up_phone(ser)
                elif option == '8':
                    hang_up_phone(ser)
                elif option == '9':
                    reject_incoming_call(ser)
                elif option == '10':
                    threading.Thread(target=temporary_disable_calls_check).start()
                    insert_pin(ser)
                elif option == '11':
                    threading.Thread(target=temporary_disable_calls_check).start()
                    check_imei(ser)
                elif option == '12':
                    threading.Thread(target=temporary_disable_calls_check).start()
                    signal_report(ser)
                elif option == '13':
                    print("Exiting the program.")
                    break
                else:
                    print("Invalid option selected.")
                input("Press Enter to continue...")

        else:
            print("GSM module not responding properly.")

        ser.close()
    except serial.SerialException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
