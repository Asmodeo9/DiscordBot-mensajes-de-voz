import discord
from discord.ext import commands
import random
import requests
from gtts import gTTS
import os

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Yo soy {bot.user}")

# Comandos básicos
@bot.command()
async def hola(ctx):
    await ctx.send("Hola!")

@bot.command()
async def clima(ctx):
    await ctx.send("https://smn.conagua.gob.mx/tools/DATA/MainSlider/MapaTiempo.jpg")

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # Convertir a ms
    await ctx.send(f'Pong! Latency: {latency:.2f}ms')

# Comando de memes
@bot.command()
async def meme(ctx):
    images = [
        "https://static.retail.autofact.cl/blog/c_url_original.1exi97kgkt7vze.jpg",
        "https://i.imgur.com/49z4BQC.gif",
        "https://i.imgur.com/lvNRWhe.jpeg",
        "https://i.imgur.com/gDQk9GQ.gif",
        "https://i.imgur.com/mLROiso.jpeg",
        "https://i.imgur.com/iXxawLm.jpeg",
        "https://i.imgur.com/NUNqvDI.jpeg",
    ]
    embed = discord.Embed(color=0x00ff00)
    embed.set_image(url=random.choice(images))
    await ctx.send(embed=embed)

# Comando llama con generación de audio
@bot.command()
async def llama(ctx, *, message):
    print(message)
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": message,
        "stream": False
    })

    if response.status_code == 200:
        data = response.json()
        llm_response = data["response"]
        
        # Configura el idioma a español
        language = "es"
        
        # Convierte el texto a voz usando gTTS
        speech = gTTS(text=llm_response, lang=language, slow=False)
        
        # Guarda el archivo de audio
        audio_file = "response.mp3"
        speech.save(audio_file)
        
        # Envía el archivo de audio como respuesta en Discord
        await ctx.send(file=discord.File(audio_file))
        
        # Opcional: elimina el archivo después de enviarlo
        os.remove(audio_file)
    else:
        print(f'Error al hacer la solicitud. Código de estado: {response.status_code}')
        await ctx.send('Hubo un error al procesar tu solicitud.')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
       
bot.run("TU TOKEN DE DISCORD")