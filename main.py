import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Get token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

# bot setup
intents = Intents.default()
intents.message_content = True  # NOQA
client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message empty -> intents not enabled)")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


# start up
@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author).split("#")[0]
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f"{username}\\in\\({channel}): {user_message}")

    await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
