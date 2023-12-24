import argparse
import logging
import sys
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException, ModbusException
from pymodbus.payload import BinaryPayloadDecoder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGISTER_TYPES = ['coil', 'input_status', 'input_register', 'holding_register']
DATA_TYPES = ['Binary', 'HEX', 'Uint16', 'Int16', 'Uint32', 'Int32', 'Float32']

def connect_to_modbus_server(ip_address, slave_id):
    client = ModbusClient(ip_address, unit=slave_id)
    client.connect()
    return client

def read_modbus_data(client, modbus_address, data_type, register_type):
    if register_type == 'coil':
        result = client.read_coils(modbus_address, 1)
    elif register_type == 'input_status':
        result = client.read_discrete_inputs(modbus_address, 1)
    elif register_type == 'input_register':
        result = client.read_input_registers(modbus_address, 1)
    else:  # holding register
        if data_type in ['Uint32', 'Int32', 'Float32']:
            result = client.read_holding_registers(modbus_address, 2)
        else:
            result = client.read_holding_registers(modbus_address, 1)
    return result

def decode_and_print_data(result, data_type):
    if not result.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        if data_type == 'Binary':
            print(bin(decoder.decode_16bit_uint()))
        elif data_type == 'HEX':
            print(hex(decoder.decode_16bit_uint()))
        elif data_type == 'Uint16':
            print(decoder.decode_16bit_uint())
        elif data_type == 'Int16':
            print(decoder.decode_16bit_int())
        elif data_type == 'Uint32':
            print(decoder.decode_32bit_uint())
        elif data_type == 'Int32':
            print(decoder.decode_32bit_int())
        elif data_type == 'Float32':
            print(decoder.decode_32bit_float())
    else:
        logger.error('Error reading modbus address')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Read Modbus address')
    parser.add_argument('-i', '--ip_address', required=True, help='IP address of the Modbus server')
    parser.add_argument('-a', '--modbus_address', required=True, type=int, help='Modbus address to read')
    parser.add_argument('-s', '--slave_id', type=int, default=1, help='Slave ID of the Modbus server')
    parser.add_argument('-r', '--register_type', default='holding_register', choices=REGISTER_TYPES, help='Type of Modbus register to read')
    parser.add_argument('-d', '--data_type', default='Uint16', choices=DATA_TYPES, help='Data type to interpret the Modbus data')
    
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    return parser.parse_args()

def main():
    args = parse_arguments()

    try:
        client = connect_to_modbus_server(args.ip_address, args.slave_id)
        result = read_modbus_data(client, args.modbus_address, args.data_type, args.register_type)
        decode_and_print_data(result, args.data_type)
    except (ConnectionException, ModbusException) as e:
        logger.error(str(e))
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()