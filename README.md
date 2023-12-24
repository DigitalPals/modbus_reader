# Modbus Reader

This Python script is a command-line tool for reading data from a Modbus server. It uses the pymodbus library to connect to the server and read data from specified Modbus addresses.

## Usage

The script is invoked from the command line with several arguments:

### Arguments
- `-i, --ip_address`: The IP address of the Modbus server. This argument is required.
- `-a, --modbus_address`: The Modbus address to read. This argument is required.
- `-s, --slave_id`: The Slave ID of the Modbus server. This argument is optional, with a default value of 1.
- `-r, --register_type`: The type of Modbus register to read. This argument is optional, with a default value of 'holding_register'. Possible choices are 'coil', 'input_status', 'input_register', 'holding_register'.
- `-d, --data_type`: The data type to interpret the Modbus data. This argument is optional, with a default value of 'Uint16'. Possible choices are 'Binary', 'HEX', 'Uint16', 'Int16', 'Uint32', 'Int32', 'Float32'.

## Functionality

The script connects to the Modbus server and reads data from the specified address. The data is then decoded according to the specified data type and printed to the console. If an error occurs during reading or decoding, an error message is printed instead.

## Error Handling

The script handles connection errors by printing an error message and closing the connection. If the read operation returns an error, an error message is printed to the console.

## Dependencies

This script requires the pymodbus library. You can install it with pip:

```pip install pymodbus```