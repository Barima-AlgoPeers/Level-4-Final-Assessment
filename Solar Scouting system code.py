# ALGO PEERS PROJECTS

# SOLAR SCOUTING SYSTEM PROJECT

# CODES:

# Import all necessary libaries:
from machine import Pin, I2C, ADC
import utime
import lcd_api
from pico_i2c_lcd import I2cLcd

# Set up I2C for the LCD screen
# We use pins GP0 for SDA (data line) and GP1 for SCL (clock line)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Create an object for the LCD
# The address (0x27) might be different for your LCD
lcd = I2cLcd(i2c, 0x27, 2, 16) # LCD 16x2

# Set up the ADC (Analog-to-Digital Converter) on pin GP26
adc = ADC(Pin(26))

# These are the reference voltage and the ADC's resolution
VREF = 3.3  # The maximum voltage the ADC can read
ADC_RESOLUTION = 65535  # The range of values the ADC can output

def read_voltage():
    # Get the raw value from the ADC (a number between 0 and 65535)
    raw_value = adc.read_u16()
    
    # Convert the raw value to a voltage (a number between 0 and 3.3)
    voltage = (raw_value / ADC_RESOLUTION) * VREF
    return voltage

def append_data_to_file(timestamp_str, voltage):
    try:
        # Open the file in append mode
        with open("voltage_data.csv", "a") as data_file:
            # Write the voltage and timestamp to the file
            data_file.write("{}, {:.2f}\n".format(timestamp_str, voltage))
    except Exception as e:
        print("Error writing to file:", e)

def main():
    while True:
        # Read the voltage from the solar panel
        voltage = read_voltage()
        
        # Clear the LCD screen
        lcd.clear()
        
        # Show the voltage on the LCD screen
        # {:.2f} means we show the voltage with two decimal places
        lcd.putstr("Voltage:{:.2f}V".format(voltage))
        
        # Get the current timestamp
        timestamp = utime.localtime()
        timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            timestamp[0], timestamp[1], timestamp[2], 
            timestamp[3], timestamp[4], timestamp[5]
        )

        # Print the timestamp and voltage to the Thonny console
        print("Timestamp: {}, Voltage: {:.2f}V".format(timestamp_str, voltage))

        # Append data to the file
        append_data_to_file(timestamp_str, voltage)
        
        # Wait for 1 second before reading the voltage again
        utime.sleep(1)
        
        led = Pin(21, Pin.OUT)
        
        # Turn on the LED
        led.value(1)
        
        utime.sleep(1)
        
        # Turn off the LED
        led.value(0)
        
        # Wait for 5 seconds before reading the voltage again
        utime.sleep(1)

try:
    
    # Initialize the file with headers if it doesn't exist
    try:
        with open("voltage_data.csv", "r") as data_file:
            pass
    except OSError:
        with open("voltage_data.csv", "w") as data_file:
            data_file.write("Timestamp,Voltage\n")
    
    
    main()
except KeyboardInterrupt:
    print("Program Interrupted")