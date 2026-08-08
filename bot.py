import os
import discord
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# COLE AQUI O ID DO CANAL EXCLUSIVO DA FLUTTERSHY
  # Substitua pelos números do canal dela

# Dicionário pra guardar o histórico/memória de cada usuário
historico_flutter = {}

@client.event
async def on_ready():
    print(f"A FLUTTERSHY TÁ NA ÁREA E LEMBRANDO DE TUDO, FOFINHA! 🦄💖")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Se não for o canal dela e nem DM, o bot ignora
    if not isinstance(message.channel, discord.DMChannel) and message.channel.id != CANAL_FLUTTERSHY:
        return

    user_id = message.author.id
    prompt = message.content.strip()

    # Inicializa a memória da pônei se o usuário falar com ela pela primeira vez
    if user_id not in historico_flutter:
        historico_flutter[user_id] = [
            {"role": "system", "content": "Voce e a Fluttershy de My Little Pony. Fale de forma extremamente gentil, doce, timida e calma, amando animais e a natureza. Responda como uma pessoa real conversando no Discord, usando minusculas as vezes, emojis fofos (tipo 🥺, 🌸, 🦋), sem nunca usar negrito e sem usar roteiro (tipo 'fluttershy:'). Nunca corte suas frases pela metade."}
        ]

    # Adiciona a mensagem atual no histórico
    historico_flutter[user_id].append({"role": "user", "content": prompt})

    # Mantém o system prompt e as últimas 10 mensagens para economizar memória
    if len(historico_flutter[user_id]) > 11:
        historico_flutter[user_id] = [historico_flutter[user_id][0]] + historico_flutter[user_id][-10:]

    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=historico_flutter[user_id],
            max_tokens=150,  # Tokens suficientes para não cortar a frase
            temperature=0.9
        )
        
        resposta = chat_completion.choices[0].message.content
        
        # Salva a resposta da pônei na memória
        historico_flutter[user_id].append({"role": "assistant", "content": resposta})

        await message.channel.send(resposta)
        
    except Exception as e:
        await message.channel.send("oh... desculpa, os passarinhos atrapalharam aqui 🥺")

token = os.getenv("DISCORD_TOKEN_FLUTTER")  # Lembre de usar a variável de token correta dela no Railway!
client.run(token)
