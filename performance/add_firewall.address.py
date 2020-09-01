#! /opt/local/bin/python3.7

import ftntlib
import time
import ipaddress
import csv
import argparse
import getpass

def add_firewall_address(fmg, adom, name, ip, netmask, debug=False):
    url = f'/pm/config/adom/{adom}/obj/firewall/address'

    data = {
        'name': name,
        'subnet': [
            ip,
            netmask,
        ],
    }
    
    if debug:
        fmg.debug('on')

    fmg.add(url, data)

    if debug:
        fmg.debug('off')

def add_firewall_addresses(fmg, params, debug=False):

    if debug:
        fmg.debug('on')

    fmg.do('add', params)

    if debug:
        fmg.debug('off')        

if __name__ == '__main__':
    firewall_address_name_prefix = 'host_'
    firewall_address_statistics_filename = 'firewall_address_statistics.csv'

    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='FortiManager IP address', required=True)
    parser.add_argument('--login', help='FortiManager login', required=True)
    parser.add_argument('--adom', help='FortiManager destination ADOM', required=True)
    parser.add_argument('--max', help='Maximum number of firewall addresses to create', required=True)
    parser.add_argument('--bunch', help='How many firewall addresses to create per FMG API request', required=True)
    parser.add_argument('--prefix', help='Prefix to use for firewall address name')
    parser.add_argument('--csv-filename', help='CSV filename where statistics will be saved')
    parser.add_argument('--debug', help='Enable debug', action='store_true')
    args = parser.parse_args()

    ip = args.ip
    login = args.login
    adom = args.adom
    max = int(args.max)
    bunch = int(args.bunch)

    if args.prefix:
        firewall_address_name_prefix = args.prefix

    if args.csv_filename:
        firewall_address_statistics_filename = csv_filename

    if args.debug:
        debug=True
    else:
        debug=False

    password = getpass.getpass()

    # Create the Statistics file for Firewall Address
    with open(firewall_address_statistics_filename, 'w') as firewall_address_statistics_fh:
        firewall_address_statistics_csv = csv.writer(firewall_address_statistics_fh,
                                                     delimiter=';')
    
        fmg = ftntlib.FortiManagerJSON()
        fmg.verbose('on')

        fmg.login(ip, login, password)

        ip = ipaddress.ip_address('10.0.0.0')

        params = []
        len_params = 0
        host_min = 0
        host_max = 0
        
        program_time_start = time.time()
        for i in range(1, max + 1):
            firewall_address_name_postfix = f'{i:05}'
            firewall_address_name = firewall_address_name_prefix + firewall_address_name_postfix

            param = {
                'data': {
                    'name': firewall_address_name,
                    'subnet': [
                        str(ip + i),
                        '255.255.255.255',
                    ],
                    'comment': 'Created with FMG API',
                },
                'url': f'/pm/config/adom/{adom}/obj/firewall/address',
            }

            params.append(param)
            len_params += 1

            if i % bunch == 0 or i == max:
                host_min = host_max + 1
                host_max = i
                host_min_with_padding = f'{host_min:05}'
                host_max_with_padding = f'{host_max:05}'
                
                time_start = time.time()
                add_firewall_addresses(fmg, params, debug=debug)
                time_end = time.time()
                time_diff = time_end - time_start
                average = len_params / time_diff
                print(f'Add Firewall Address(es) [{firewall_address_name_prefix}{host_min_with_padding} - {firewall_address_name_prefix}{host_max_with_padding}]: {time_diff} sec; Average Object/Second: {average}')
                
                firewall_address_statistics_csv.writerow([f'{host_min} - {host_max}', time_end - time_start])
                params = []
                len_params = 0

        program_time_end = time.time()

        program_time_diff = program_time_end - program_time_start
        program_average = max / program_time_diff
        print(f'Total Time: {program_time_diff} sec; Average Object/Second: {program_average}')
    
        fmg.logout()
