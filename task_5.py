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
    voltage_array = []
    while time_s < 20:
        time_s = time_s + 1
        time.sleep(1.)
        read_data = ms.read(dev_id=6, var_id=5, offset=256 + 20, d_len=2, data=None)
        temp = (read_data[1] * 256 + read_data[0]) / 256
        read_data = ms.read(dev_id=6, var_id=5, offset=256 + 16, d_len=2, data=None)
        voltage = (read_data[1] * 256 + read_data[0]) / 256
        print(temp)
        temp_array.append(temp)
        voltage_array.append(voltage)
    # график температуры и напряжения
    fig, (ax1, ax2) = plt.subplots(2, 1)
    #
    ax1.plot(temp_array, label="T")
    ax1.legend()
    ax1.set(ylabel='Температура', title='Температура и Напряжение')
    ax1.grid()
    #
    ax2.plot(voltage_array, label="U")
    ax2.legend()
    ax2.set(xlabel='Время, с', ylabel='Напряжение')
    ax2.grid()
    #
    plt.show()
    #