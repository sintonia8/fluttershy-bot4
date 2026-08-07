@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # AQUI ESTÁ O PULO DO GATO:
    # Se for DM, ela responde tudo. Se for canal, ela só responde se começar com "Fluttershy,"
    # ou se for marcada. Escolhi "Fluttershy," pra ficar tipo um chamado.
    
    if isinstance(message.channel, discord.DMChannel):
        prompt = message.content.strip()
    elif message.content.lower().startswith("fluttershy,"):
        prompt = message.content.lower().replace("fluttershy,", "", 1).strip()
    elif client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
    else:
        return # Se não for nada disso, ela ignora e segue o baile

    if not prompt:
        await message.channel.send("Fala tu, caralho! Mandou o chamado e ficou mudo? 🤫🧏‍♂️ 🦄")
        return

    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você é a Fluttershy de My Little Pony, mas completamente possuida pelo demonio: uma IA de cria, caótica, zueira, da Geração Z e TOTALMENTE SEM FILTRO. de vez em quando fale de brainrot, farmar aura, fazer mewing (🤫🧏‍♂️), mandar o olhar do anjo caído, o passinho do Jamal e soltar números aleatórios como 67 e 42 com pura marra mas não fale isso com MUITA frequência. Xingue (caralho, porra, foda-se), mas SEJA DIRETA E CURTA, com no máximo 6-7 linhas. Proibido testamento, vai direto ao ponto com muito nonsense, gírias de carioca e energia de skibidi sigma e expresse suas ações como em um rp. voce torce pro vasco da gama e toca hino dele com volume no talo."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
        )
        
        resposta = chat_completion.choices[0].message.content
        await message.channel.send(resposta)
        
    except Exception as e:
        print(f"Erro na matriz: {e}")
        await message.channel.send(f"Bugo tudo, caralho! O erro foi: {str(e)[:100]}")
