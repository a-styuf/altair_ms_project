import serial
import serial.tools.list_ports
import time


class MSDev:
    def __init__(self, **kw):
        # parent init
        self.serial = serial.Serial()
        # parameters
        self.serial.baudrate = kw.get('baudrate', 9600)
        self.serial.timeout = kw.get('timeout', 0.1)
        self.serial.port = kw.get("port", "COM0")
        self.debug = kw.get("debug", False)
        #
        self.read_data = []
        self.write_data = []
        #
        pass

    def connection(self, **kw):
        #
        if self.serial.is_open:
            self.serial.close()
        #
        self.serial.baudrate = kw.get('baudrate', self.serial.baudrate)
        self.serial.timeout = kw.get('timeout', self.serial.timeout)
        self.serial.port = kw.get("port", self.serial.port)
        self.debug = kw.get("debug", self.debug)
        #
        self.serial.open()

        pass

    def disconnection(self):
        try:
            self.serial.close()
        except Exception as error:
            print(error)
        pass

    def write(self, dev_id=6, var_id=5, offset=0, d_len=0, data=None):
        self.request(mode="write", dev_id=dev_id, var_id=var_id, offset=offset, d_len=d_len, data=data)
        pass

    def read(self, dev_id=6, var_id=5, offset=0, d_len=0, data=None):
        read_data = self.request(mode="read", dev_id=dev_id, var_id=var_id, offset=offset, d_len=d_len, data=data)
        return list(read_data)[8:]

    def get_ms_temp(self):
        read_data = self.read(dev_id=6, var_id=5, offset=256+20, d_len=2, data=None)
        temp = (read_data[1]*256 + read_data[0]) / 256
        return temp

    def get_pn_v_and_i(self):
        voltage_arr = []
        curr_arr = []
        for i in range(5):
            read_data = self.read(dev_id=6, var_id=5, offset=256+16+i*18, d_len=2, data=None)
            voltage_arr.append((read_data[1]*256 + read_data[0]) / 256)
            read_data = self.read(dev_id=6, var_id=5, offset=256 + 18+i*18, d_len=2, data=None)
            curr_arr.append((read_data[1] * 256 + read_data[0]) / 256)
        return voltage_arr, curr_arr

    def request(self, mode="read", dev_id=0, var_id=0, offset=0, d_len=0, data=None):
        #
        can_num = 1
        rtr = 0 if mode == "write" else 1
        if data is None:
            data = []
        real_len = min(d_len, len(data)) if mode == "write" else d_len
        part_offset = 0
        read_data = []
        while real_len > 0:
            part_len = 8 if real_len >= 8 else real_len
            real_len -= 8
            finish = 1 if real_len <= 0 else 0
            id_var = ((dev_id & 0x0F) << 28) | ((var_id & 0x0F) << 24) | (((part_offset+offset) & 0x1FFFFF) << 3) | \
                     ((0x00 & 0x01) << 2) | ((rtr & 0x01) << 1) | ((0x00 & 0x01) << 0)
            packet_list = [can_num & 0x01, 0x00,
                           (id_var >> 0) & 0xFF, (id_var >> 8) & 0xFF,
                           (id_var >> 16) & 0xFF, (id_var >> 24) & 0xFF,
                           (part_len >> 0) & 0xFF, (part_len >> 8) & 0xFF]
            packet_list.extend(data[0 + part_offset:part_len + part_offset])
            part_offset += 8
            self.serial.write(bytes(packet_list))
            read_data += self.serial.read(8+part_len)
        id_var = ((dev_id & 0x0F) << 28) | ((var_id & 0x0F) << 24) | ((offset & 0x1FFFFF) << 3) | \
                 ((0x00 & 0x01) << 2) | ((rtr & 0x01) << 1) | ((0x00 & 0x01) << 0)
        self._print("Try to send command <0x%08X> (%s):" % (id_var, self._id_var_to_str(id_var)))
        return read_data

    def __repr__(self):
        report_str = "MS: "
        #
        connection_str = "open" if self.serial.is_open else "close"
        report_str += "%s" % connection_str
        report_str += ", " + "baudrate=%d" % self.serial.baudrate
        report_str += ", " + "timeout=%.3f" % self.serial.timeout
        #
        return report_str

    def _print(self, *args):
        if self.debug:
            print_str = "MS debug: " + self.get_time()
            for arg in args:
                print_str += " " + str(arg)
            print(print_str)

    @staticmethod
    def get_time():
        return time.strftime("%H-%M-%S", time.localtime()) + "." + ("%.3f:" % time.perf_counter()).split(".")[1]

    @staticmethod
    def process_id_var(id_var):
        """
        process id_var_value
        :param id_var: id_var according to title
        :return: егзду of id_var fields
        """
        dev_id = (id_var >> 28) & 0x0F
        var_id = (id_var >> 24) & 0x0F
        offset = (id_var >> 3) & 0x01FFFFF
        res2 = (id_var >> 2) & 0x01
        rtr = (id_var >> 1) & 0x01
        res1 = (id_var >> 0) & 0x01
        return res1, rtr, res2, offset, var_id, dev_id

    def _id_var_to_str(self, id_var):
        ret_str = ""
        ret_str += "dev_id:%2d " % self.process_id_var(id_var)[5]
        ret_str += "var_id:%2d " % self.process_id_var(id_var)[4]
        ret_str += "offs:%3d " % self.process_id_var(id_var)[3]
        ret_str += "rtr:%d-%s " % (self.process_id_var(id_var)[1], "rd" if self.process_id_var(id_var)[1] else "wr")
        return ret_str


def get_com_list():
    com_list = serial.tools.list_ports.comports()
    return [com.name + ": " + com.description for com in com_list]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ms = MSDev(port="COM7", baudrate=9600)
    print(ms)
    ms.connection()
    print(ms)
    ms.write(dev_id=6, var_id=4, offset=39, d_len=1, data=[0xA5])
    read_data = ms.read(dev_id=6, var_id=5, offset=0, d_len=128)
    print(["%02X " % var for var in read_data])

