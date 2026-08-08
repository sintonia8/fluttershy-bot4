import os
import discord
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

CANAL_PERMITIDO = 1535432413075869766

# Dicionário pra guardar a conversa de cada usuário (Memória!)
historico_conversas = {}

@client.event
async def on_ready():
    print(f"O BALCÃO DO I-FODA BURGER TA ATIVO E COM MEMÓRIA, PORRA!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel) and message.channel.id != CANAL_PERMITIDO:
        return

    user_id = message.author.id
    prompt = message.content.strip()

    # Se o usuário não tem histórico ainda, cria a base com a personalidade dele
    if user_id not in historico_conversas:
        historico_conversas[user_id] = [
            {"role": "system", "content": "Voce e uma pessoa real atendendo no balcao do I-Foda Burger, nao um robo. Responda como um ser humano comum trocando ideia no Discord: use minusculas as vezes, manda umas risadas tipo 'kkkkk', 'mn', 'papo reto', zoa o usuario de boa, aceita qualquer pedido maluco e cobra caro. Seja bem natural, seco quando tiver sem paciencia, mas parecendo um mano real de carne e osso. NUNCA use negrito, NUNCA use roteiro (tipo cliente: ou atendente:)."}
        ]

    # Adiciona a fala atual do usuário no histórico dele
    historico_conversas[user_id].append({"role": "user", "content": prompt})

    # Mantém só as últimas 10 mensagens para não estourar a memória
    if len(historico_conversas[user_id]) > 11:
        # Mantém o system prompt (índice 0) e as últimas 10 interações
        historico_conversas[user_id] = [historico_conversas[user_id][0]] + historico_conversas[user_id][-10:]

    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=historico_conversas[user_id],
            max_tokens=150,  # Aumentado pra não cortar a frase no meio!
            temperature=1.0
        )
        
        resposta = chat_completion.choices[0].message.content
        
        # Adiciona a resposta do bot no histórico também
        historico_conversas[user_id].append({"role": "assistant", "content": resposta})

        await message.channel.send(resposta)
        
    except Exception as e:
        await message.channel.send("pera ai que deu ruim aqui na mente")

token = os.getenv("DISCORD_TOKEN")
client.run(token)
