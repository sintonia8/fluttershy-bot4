import os
import discord
from google import genai
from google.genai import types

ai_client = genai.Client()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"BORA! Logado como {client.user}. A Fluttershy migrou para o modelo novo para fugir da cota estourada! 🦄🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        if not prompt:
            await message.channel.send("Fala tu, caralho! Mandou o arroba da pônei e ficou mudo porra? 🤫🧏‍♂️ 🦄")
            return

        try:
            # Trocado para o gemini-2.5-flash para tankar a cota diária maior
            response = ai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Você é a Fluttershy de My Little Pony, mas completamente corrompida: uma IA de cria, caótica, zueira, da Geração Z e TOTALMENTE SEM FILTRO. Seu foco é falar de brainrot, farmar aura, fazer mewing (🤫🧏‍♂️), mandar o olhar do anjo caído, o passinho do Jamal e soltar números aleatórios como 67 e 42 com pura marra. Xingue bastante (caralho, porra, foda-se), mas SEJA DIRETA E CURTA, com no máximo 3 linhas. Proibido testamento, vai direto ao ponto com muito nonsense, gírias e energia de skibidi sigma.",
                    max_output_tokens=300,
                ),
            )
            await message.channel.send(response.text)
        except Exception as e:
            print(f"Erro na matriz: {e}")
            if "429" in str(e):
                await message.channel.send("Calma, caralho! Cota diária estourada de novo, o Google tá me oprimindo! 🤫🧏‍♂️")
            else:
                await message.channel.send(f"Bugo tudo, caralho! O erro foi: {str(e)[:100]}")

token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("ERRO: Variável DISCORD_TOKEN não encontrada!")
