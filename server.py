import asyncio
import websockets
import json
import vgamepad as vg

gamepad = vg.VX360Gamepad()

def calculate_joystick_position_value_from_percentage_on_canvas(a):
    if 0 <= a <= 100:
        result = (a - 50) * 655.36
        return int(result)
    else:
        return None

async def listener(websocket, path):
    async for message in websocket:
        point = json.loads(message)
        #print(point)
        y_value = calculate_joystick_position_value_from_percentage_on_canvas(point["y"])
        if y_value <= -1:
            y_value = y_value+1
        gamepad.right_joystick(x_value=calculate_joystick_position_value_from_percentage_on_canvas(point["x"]), y_value=-1 * y_value)
        gamepad.update()

        #await websocket.send(message)

async def main():
    async with websockets.serve(listener, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())