import pyvisa
import time

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()

# GPIB addresses
HP83650B_ADDRESS = 'GPIB0::27::INSTR'  # Replace with the actual GPIB address of HP 83650B
E4419B_ADDRESS = 'GPIB0::16::INSTR'   # Replace with the actual GPIB address of E4419B

# Connect to instruments
signal_generator = rm.open_resource(HP83650B_ADDRESS)
power_meter = rm.open_resource(E4419B_ADDRESS)

# Timeout
signal_generator.timeout = 30000  # Timeout in milliseconds, adjust as needed
power_meter.timeout = 30000       # Adjust as needed
#5e+7, 10e+7, 50e+7,1e+9,2e+9,3e+9,4e+9,5e+9,6e+9,7e+9,8e+9,9e+9,10e+9,11e+9,

# Define your frequency list
frequency_list = [5e+7, 10e+7, 50e+7,1e+9,2e+9,3e+9,4e+9,5e+9,6e+9,7e+9,8e+9,9e+9,10e+9,11e+9,12e+9,13e+9,14e+9,15e+9,16e+9,
                  17e+9,18e+9]
                  #19e+9,20e+9,21e+9,22e+9,23e+9,24e+9,25e+9,26e+9,27e+9,28e+9,29e+9,30e+9,31e+9,32e+9,33e+9,34e+9,
                  #35e+9,36e+9,37e+9,38e+9,39e+9,40e+9,41e+9,42e+9,43e+9,44e+9,45e+9,46e+9,47e+9,48e+9,49e+9,50e+9]  # Example frequencies in Hz

# Store measurements
measurements_channel_a = []
measurements_channel_b = []

def PowerLeveling():

    # Set a tolerance level for the measurement
    tolerance = 0.01  # Adjust this value as needed
    adjustment_step = 0.001  # Adjust the step size as necessary
    max_attempts = 5000      # Prevent infinite loops
    attempts = 0
    current_adjustment = 0.0  # Initialize current adjustment

    while True:
        power_meter.write(f'UNIT2:POW dBm')
        time.sleep(0.5)
        #    try:
        std_pl = float(power_meter.query(f'FETC2?'))
        print("Current std power level:", std_pl)
        #if std_pl > 20:
        #    break

        if -tolerance <= std_pl <= tolerance:
            break

        # Determine adjustment step
        if abs(std_pl) > 1:
            adjustment_step = 1  # Larger adjustment for larger deviations
        elif abs(std_pl) > 0.5:
            adjustment_step = 0.1  # Medium adjustment
        elif abs(std_pl) > 0.1:
            adjustment_step = 0.05  # Smaller adjustment
        else:
            adjustment_step = 0.01  # Finest adjustment

        # Adjust current_adjustment
        if std_pl > 0:
            current_adjustment -= adjustment_step
        else:
            current_adjustment += adjustment_step


        print(f'Current Adjustment: {current_adjustment}')
        signal_generator.write(f'POW:LEVEL {current_adjustment} dBm')

        # Optional: Add a delay
        time.sleep(0.5)  # Delay for 1 second, adjust as necessary

        attempts += 1
        if attempts > max_attempts:
            print(f"Maximum attempts reached, stopping adjustment.")
            break

#        except pyvisa.errors.VisaIOError as e:
#            print(f"VISA IO Error: {e}")
#            break  # or handle the error as needed
#        except Exception as e:
#            print(f"Unexpected Error: {e}")
#            break  # or handle differently


def measure_frequencies():

    signal_generator.write(f'SYSTEM:PRESET')
    power_meter.write(f"SYSTEM:PRESET")
    power_meter.write(f'UNIT1:POW WATT')
    time.sleep(0.5)
    power_meter.write(f'UNIT2:POW WATT')
    time.sleep(0.5)
    print(f'waiting for power stabalization 5s')
    time.sleep(5)
    power_meter.write(f'CALibration1:ZERO:AUTO ONCE')
    print("zeroing channel 1: waiting 15s")
    time.sleep(15)
    power_meter.write(f'CALibration2:ZERO:AUTO ONCE')
    print("zeroing channel 2: waiting 15s")
    time.sleep(15)

    for freq in frequency_list:
        try:
            # Set frequency on the signal generator
            print("setting frequency")
            signal_generator.write(f'FREQ:CW {freq} Hz')
            signal_generator.write(f'POW:STAT ON')
            PowerLeveling()
            # setting units
            print("setting units")
            power_meter.write(f'UNIT1:POW WATT')
            time.sleep(0.5)
            power_meter.write(f'UNIT2:POW WATT')
            time.sleep(0.5)

            # Measure and store power for each channel
            channel_a_power = float(power_meter.query(f'FETC1?'))
            channel_b_power = float(power_meter.query(f'FETC2?'))

            measurements_channel_a.append((freq, channel_a_power))
            measurements_channel_b.append((freq, channel_b_power))
            signal_generator.write(f'POW:STAT OFF')


            # Print or process the collected measurements
            print("Measurements Channel A:", measurements_channel_a)
            print("Measurements Channel B:", measurements_channel_b)

        except pyvisa.errors.VisaIOError as e:
            print(f"VISA IO Error: {e}")
            print(f'hitting errors mang')
            continue  # Skip to the next frequency or handle as needed
        except Exception as e:
            print(f"Unexpected Error: {e}")
            print(f'hitting second exception mang')
            continue  # or handle differently

def CFPerentage():

# Define the data
    measurements_pass_1_a =measurements_channel_a 
    measurements_pass_2_a =measurements_channel_b
# Ensure both lists have the same length and corresponding frequencies match
    assert len(measurements_pass_1_a) == len(measurements_pass_2_a)

# Calculate averages and convert to percentages
    averaged_percentages_a = []
    for i in range(len(measurements_pass_1_a)):
        freq, meas_1 = measurements_pass_1_a[i]
        _, meas_2 = measurements_pass_2_a[i]

        avg_meas = ((meas_1 + meas_2) / 2) * 100
        averaged_percentages_a.append((freq, avg_meas))

# Repeat the process for Channel B data
# measurements_pass_1_b = [...]
# measurements_pass_2_b = [...]
# averaged_percentages_b = [...]

# Process and print the results
    for freq, avg_meas in averaged_percentages_a:
        print(f"Frequency: {freq} Hz, Average Measurement (Channel A): {avg_meas:.4f}%")

# Similar printing for Channel B results


measure_frequencies()
CFPerentage()
signal_generator.close()
power_meter.close()


