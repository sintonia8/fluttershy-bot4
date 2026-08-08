import os
import discord
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

historico_conversas = {}

@client.event
async def on_ready():
    print(f"O BALCÃO DO I-FODA BURGER ESTÁ ABERTO EM TODO LUGAR, PORRA! 🍔🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # TRAVA REMOVIDA: ELE VAI RESPONDER EM TODOS OS CANAIS!
    user_id = message.author.id
    prompt = message.content.strip()

    if user_id not in historico_conversas:
        historico_conversas[user_id] = [
            {"role": "system", "content": "Voce e uma pessoa real atendendo no balcao do I-Foda Burger, nao um robo. Responda como um ser humano comum trocando ideia no Discord: use minusculas as vezes, manda umas risadas tipo 'kkkkk', 'mn', 'papo reto', zoa o usuario de boa, aceita qualquer pedido maluco e cobra caro. Seja bem natural, seco quando tiver sem paciencia, mas parecendo um mano real de carne e osso. NUNCA use negrito, NUNCA use roteiro (tipo cliente: ou atendente:)."}
        ]

    historico_conversas[user_id].append({"role": "user", "content": prompt})

    if len(historico_conversas[user_id]) > 11:
        historico_conversas[user_id] = [historico_conversas[user_id][0]] + historico_conversas[user_id][-10:]

    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=historico_conversas[user_id],
            max_tokens=150,
            temperature=1.0
        )
        resposta = chat_completion.choices[0].message.content
        historico_conversas[user_id].append({"role": "assistant", "content": resposta})
        await message.channel.send(resposta)
    except Exception as e:
        await message.channel.send("pera ai que deu ruim aqui na mente")

token = os.getenv("DISCORD_TOKEN")
client.run(token)
