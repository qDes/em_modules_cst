import struct


def decode_wifi_data(data: list) -> tuple:
    header, number, t0, t1,  t2, half, encoderL, f0, f1, sum = struct.unpack('<ccBBBBBhhB', data)
    timer = bytearray(4)
    #print(type(t0))
    timer[0] = t0
    timer[1] = t1
    timer[2] = t2
    timer[3] = half & 0xF0
    timer_long = struct.unpack('<L', timer)

    encoder = bytearray(2)
    encoder[0] = encoderL
    encoder[1] = half & 0x0F
    encoder_int = struct.unpack('<H', encoder)

    return (header, ord(number), timer_long[0], encoder_int[0], f0, f1, sum)

if __name__ == '__main__':
    with open('1.log', 'rb') as f:
        data = f.read(12)
        while data:
            print(*decode_wifi_data(data))#header, ord(number), timer_long[0], encoder_int[0], f0, f1, sum))
            data = f.read(12)
