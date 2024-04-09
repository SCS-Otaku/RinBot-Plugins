from pyrogram import Client, filters
from PIL import Image
import requests
from io import BytesIO
import os
from . import HelpMenu, hellbot, on_message
from pyrogram.types import Message


# Initialize the Pyrogram Client
app = Client("my_image_upscale_bot")

# Function to upscale the image
def upscale_image(client, message):
    chat_id = message.chat.id
    
    if message.photo is None:
        client.send_message(chat_id, "Please send an image to upscale.")
        return
    
    file_id = message.photo.file_id

    file = client.get_photo(file_id)
    image_url = file.file_path

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    image = image.resize((image.size[0]*2, image.size[1]*2))

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)

    client.send_photo(chat_id, photo=output)

# Registering the upscale_image function as a message handler
@app.on_message("ups", allow_stan=True)
async def upscale_command(client, message):
    await upscale_image(client, message)

# Start the bot
app.run()
