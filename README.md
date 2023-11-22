# RF/Microwave Power Sensor Calibration Script for 1 mW (0dBm) range sensors

## Overview
This Python script is designed for calibrating RF/Microwave equipment, specifically for power measurements across a range of frequencies. It automates the calibration process using a signal generator and power meter, and calculates the calibration factor as a percentage of Channel A's power relative to Channel B's power.

## Features
- Automated frequency setting and power measurement.
- Power leveling to maintain consistent measurement accuracy.
- Dual pass measurement for increased reliability.
- Calculation of calibration factor as a percentage.
- Averaging of measurements over two passes.

## Requirements
- Python 3.x
- PyVISA library
- Compatible GPIB interface and drivers

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install PyVISA using pip:
# 2PassSplitter
PyVisa implementation of the 2 Pass Splitter method for transfering cal factor from standard sensors

## Usage
1. Update the GPIB addresses in the script to match your equipment setup:
- `HP83650B_ADDRESS` for the signal generator.
- `E4419B_ADDRESS` for the power meter.
2. Modify the `frequency_list` in the script to include the frequencies you want to test.
3. Run the script:

## Customization
You can customize the script by modifying the frequency list or adjusting the power leveling tolerance and steps according to your specific requirements.

## Contribution
Contributions to enhance the script or add new features are welcome. Please submit a pull request or open an issue to discuss your ideas.

## License
This project is licensed under [appropriate license type] - see the LICENSE file for details.

## Acknowledgments
- [Any collaborators or sources of inspiration]
- [Any institutions or organizations that supported this work]

## Contact
For any queries or assistance, feel free to contact [Your Name or Contact Information].

---

Note: This script is intended for professional use and requires proper understanding of RF/Microwave calibration principles. Please use it responsibly.
