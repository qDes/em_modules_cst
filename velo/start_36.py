import asyncio

async def start():

    cmd_control = ['python','velo_q5.py']
    cmd_plot = ['python','plotting_udp.py']
    create_control = asyncio.create_subprocess_exec(*cmd_control,
            stdout = asyncio.subprocess.PIPE)
    create_plot = asyncio.create_subprocess_exec(*cmd_plot,
            stdout = asyncio.subprocess.PIPE)

    control = await create_control
    plot = await create_plot
    while True:
        await control.wait()
        await plot.wait()

asyncio.run(start())

