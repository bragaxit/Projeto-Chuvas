— COLETA DE DADOS
nome = input("Qual o seu nome? ").strip().title()
cidade = input("Qual o nome da sua cidade? ").strip().title()

try:
    temp = float(input("Quantos graus está fazendo agora? "))
    chance_cv = int(input("Qual a chance de chuva hoje? (0 a 100) "))
    volume_cv = float(input("Qual o volume de chuva previsto em MM? "))
except ValueError:
    print("\n[ERRO] Por favor, use apenas números para temperatura e chuva. Reinicie o programa.")
    exit()

# --- STATUS DE VOLUME E CHANCE DE CHUVA ---
if chance_cv >= 80 and volume_cv >= 50:
    status_alagamento = "Alerta VERMELHO: Risco ALTO de alagamento e volume crítico."
    status_energia = "Possibilidade de queda de energia: ALTA."
elif chance_cv >= 50 and volume_cv >= 20:
    status_alagamento = "Alerta AMARELO: Risco moderado. Escoamento pode ficar lento."
    status_energia = "Possibilidade de queda de energia: MÉDIA/BAIXA."
elif chance_cv < 30:
    status_alagamento = "Alerta VERDE: Pouca chance de chuva."
    status_energia = "O risco de queda de energia é BAIXO/NULO."
else:
    status_alagamento = "OBSERVAÇÃO: Chuva leve prevista. Sem grandes riscos."
    status_energia = "Risco de queda de energia é MÍNIMO."

# --- MENSAGEM DE CLIMA E LISTA DE ITENS ---
itens_mochila = ["Carteira", "Celular"]

if temp > 30:
    msg_clima = "Você deve usar protetor solar!"
    itens_mochila.extend(["Protetor Solar", "Garrafa de Água", "Boné"])
    # Óculos de sol no calor só se não chover
    if chance_cv < 50:
        itens_mochila.append("Óculos de sol")

elif temp >= 20:
    msg_clima = "O clima está agradável hoje."
    # Lógica dos óculos: só entra se a chance de chuva for baixa
    if chance_cv < 50:
        itens_mochila.append("Óculos de sol")

else:
    msg_clima = "Hoje está muito frio!"
    itens_mochila.append("Casaco")

# Adiciona guarda-chuva se houver risco real (independente da temperatura)
if chance_cv >= 50:
    itens_mochila.append("Guarda-chuva ou Capa")

# --- TEXTO FINAL ---
print("\n" + "-" * 90)
print(f"Olá {nome}! Relatório para {cidade}:")
print(f"Clima: {msg_clima}")
print(f"Probabilidade de chuva: {chance_cv}%")
print(f"Alerta: {status_alagamento}")
print(f"Energia: {status_energia}")
print("-" * 90)

# Removendo duplicatas (caso algum item tenha sido adicionado duas vezes)
itens_finais = list(dict.fromkeys(itens_mochila))

print(f"Dica: Não esqueça de levar: {', '.join(itens_finais)}.")
print("-" *  80)
