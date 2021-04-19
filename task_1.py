import ms_device
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(ms_device.get_com_list())
    time.sleep(0.1)
    ms = ms_device.MSDev(port="COM12", baudrate=9600, timeout=0.05)
    ms.connection()
    time.sleep(0.1)
    # мигание светодиодом
    ms.write(dev_id=6, var_id=4, offset=48, d_len=1, data=[127])
    time.sleep(0.1)

