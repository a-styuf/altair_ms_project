import ms_device
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(ms_device.get_com_list())
    time.sleep(0.1)
    ms = ms_device.MSDev(port="COM9", baudrate=9600, timeout=0.05)
    ms.connection()
    time.sleep(0.1)
    # температура МС
    read_data = ms.read(dev_id=6, var_id=5, offset=256 + 20, d_len=2, data=None)
    temp = (read_data[1] * 256 + read_data[0]) / 256
    print(temp)
