import asyncio
from pathlib import Path

from pyrogram import Client

from tgintegration import BotController
from tgintegration import Response

# Target chat. Can also be a list of multiple chat ids/usernames
TARGET = "party_victorina_bot"
clicked = 11

# This example uses the configuration of `config.ini` (see examples/README)
examples_dir = Path(__file__).parent.parent.absolute()
SESSION_NAME: str = "tgintegration_examples"


# This example uses the configuration of `config.ini` (see examples/README)
def create_client(session_name: str = SESSION_NAME) -> Client:
    return Client(
        "my_account",
        api_id=28543768,
        api_hash="021b8f94f5539ee31218a0adb5adcf6f"
    )


async def run_example(client: Client):
    controller = BotController(
        peer="@party_victorina_bot",  # We are going to run tests on https://t.me/BotListBot
        client=client,
        max_wait=20,  # Maximum timeout for responses (optional)
        wait_consecutive=20,  # Minimum time to wait for more/consecutive messages (optional)
        raise_no_response=True,  # Raise `InvalidResponseError` when no response received (defaults to True)
        global_action_delay=2.5,  # Choosing a rather high delay so we can follow along in realtime (optional)
    )

    print("Clearing chat to start with a blank screen...")
    await controller.clear_chat()

    print("Sending /start and waiting for exactly 3 messages...")
    async with controller.collect(count=1) as response:  # type: Response
        await controller.send_command("/start ")

    async with controller.collect(count=3) as response:  # type: Response
        await client.send_message(controller.peer_id, "Создать")

    async with controller.collect(count=1) as response:  # type: Response
        await client.send_message(controller.peer_id, "1")

    async with controller.collect(count=1) as response:  # type: Response
        await client.send_message(controller.peer_id, "Films & TV")

    async with controller.collect(count=1) as response:  # type: Response
        await client.send_message(controller.peer_id, "10")

    async with controller.collect(count=1) as response:  # type: Response
        await controller.send_command("/beginGame ")

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    await asyncio.sleep(3)
    keyboard = response.messages[0]
    async with controller.collect(count=1) as response:  # type: Response
        await keyboard.click(0, 0)

    assert response.messages[0].text == 'Ждём остальных...'
    print("Success!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run_example(create_client()))