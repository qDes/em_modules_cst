import asyncio
import struct 


def decode_wifi(data: list) -> tuple:
    try:
        header, number, t0, t1,  t2, half, encoderL, f0, f1, sum1 = struct.unpack('<ccBBBBBhhB', data)
    except struct.error:
        return None
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


async def read_pedal(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        pedal_tenzo = await reader.read(2048)
        # check header
        if chr(pedal_tenzo[0]) == '$':
            message = pedal_tenzo[:12]
            data = decode_wifi(message)
            print(f"f0={data[4]},f1={data[5]}")
 

if __name__=="__main__":
    asyncio.run(read_pedal('192.168.0.101',23))
