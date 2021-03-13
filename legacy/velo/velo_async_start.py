import asyncio

async def start():

    cmd_control = ['python','velo_q5.py']
    cmd_plot = ['python','plotting_udp.py']
    cmd_pedal = ['python', 'pedal/plot_pedal.py']
    create_control = asyncio.create_subprocess_exec(*cmd_control,
            stdout = asyncio.subprocess.PIPE)
    create_plot = asyncio.create_subprocess_exec(*cmd_plot,
            stdout = asyncio.subprocess.PIPE)
    create_pedal = asyncio.create_subprocess_exec(*cmd_pedal,
            stdout=asyncio.subprocess.PIPE)
    control = await create_control
    plot = await create_plot
    pedal = await create_pedal
    while True:
        await control.wait()
        await plot.wait()
        await pedal.wait()

loop = asyncio.get_event_loop()
loop.run_until_complete(start())
loop.close()
#asyncio.run(start())
