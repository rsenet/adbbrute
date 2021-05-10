#!/usr/bin/env python3
from lib import brute
import argparse

__author__  = 'Regis SENET'
__email__   = 'regis.senet@bssi.fr'
__git__     = 'https://github.com/rsenet/adbbrute'
__version__ = '0.1'
short_desc  = "Android LockScreen Bruteforce"

arg_parser = argparse.ArgumentParser(description=short_desc)
arg_parser.add_argument('--device', help="Specify the device to bruteforce ")
arg_parser.add_argument('--type', help="Type of bruteforce (gui / locksettings)")
u_args = arg_parser.parse_args()
device = u_args.device
typebf = u_args.type

try:
    if not u_args.device:
        print("[x] Please specify the device to bruteforce (--device)")
        brute.display_connected_device()

    else:
        if typebf is not None:
            if brute.check_device_exists(device):
                # Get device info
                brute.show_device_info(device)

                if typebf == "gui":
                    brute.start_gui_bf(device)

                if typebf == "locksettings":
                    brute.start_locksettings_bf(device)

            else:
                print("[x] Device does not exists - Leaving")

        else:
            print("[x] Type of bruteforce missing (--type). Please specify it")

except KeyboardInterrupt:
    print("[x] Leaving")