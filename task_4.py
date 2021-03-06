import ms_device
import time
import matplotlib
import matplotlib.pyplot as plt

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(ms_device.get_com_list())
    time.sleep(0.1)
    ms = ms_device.MSDev(port="COM9", baudrate=9600, timeout=0.05)
    ms.connection()
    time.sleep(0.1)
    # температура МС в течении минуты
    time_s = 0
    temp_array = []
    while time_s < 20:
        time_s = time_s + 1
        time.sleep(1.)
        # чтение температуры
        read_data = ms.read(dev_id=6, var_id=5, offset=256 + 20, d_len=2, data=None)
        temp = (read_data[1] * 256 + read_data[0]) / 256
        print(temp)
        temp_array.append(temp)
    # график температуры
    plt.plot(temp_array, label="T")
    plt.ylabel('Температура, °C')
    plt.xlabel('Время, с')
    plt.title('Температура')
    plt.grid()
    #
    plt.show()
    #