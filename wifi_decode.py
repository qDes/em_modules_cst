import struct


def decode_wifi_data(data: list) -> tuple:
    header, number, t0, t1,  t2, half, encoderL, f0, f1, sum1 = struct.unpack('<ccBBBBBhhB', data)
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

    return (header, ord(number), timer_long[0], encoder_int[0], f0, f1, sum1)

if __name__ == '__main__':
    with open('log/3.log', 'rb') as f:
        '''
        b0 = f.read(1)
        b1 = f.read(1)
        b2 = f.read(1)
        b3 = f.read(1)
        b4 = f.read(1)
        b5 = f.read(1)
        b6 = f.read(1)
        b7 = f.read(1)
        b8 = f.read(1)
        b9 = f.read(1)
        b10 = f.read(1)
        b11 = f.read(1)
        byte_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11]
        byte_sum = b0 + b1 + b2 + b3 + b4 + b5 + b6 + b7 + b8 + b9 + b10
        data = f.read(12)

        '''
        data = f.read(1)
        
        while data:
            if data == b'$':
                data += f.read(11)
                print(*decode_wifi_data(data))
            data = f.read(1)
        

