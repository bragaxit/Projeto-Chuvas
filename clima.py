#CONSTANTES DE ALERTA
LIMITE_CHANCE_ALTA    = 80
LIMITE_VOLUME_CRITICO = 50
LIMITE_CHANCE_MEDIA   = 50
LIMITE_VOLUME_MEDIO   = 20
LIMITE_CHANCE_BAIXA   = 30
TEMP_QUENTE = 30
TEMP_AGRADAVEL = 20

# FUNÇÕES
def coletar_dados():
    """Coleta e valida todos os dados do usuário."""
    nome   = input("Qual o seu nome? ").strip().title()
    cidade = input("Qual o nome da sua cidade? ").strip().title()

    try:
        temp      = float(input("Quantos graus está fazendo agora? "))
        chance_cv = int(input("Qual a chance de chuva hoje? (0 a 100): "))
        volume_cv = float(input("Qual o volume de chuva previsto em MM? "))
    except ValueError:
        print("\n[ERRO] Use apenas números para temperatura e chuva. Reinicie o programa.")
        exit()

    # Validação de intervalos
    if not (-20 <= temp <= 60):
        print("\n[ERRO] Temperatura invalida")
        exit()
    if not (0 <= chance_cv <= 100):
        print("\n[ERRO] Chance de chuva deve ser entre 0 e 100.")
        exit()
    if volume_cv < 0:
        print("\n[ERRO] Volume de chuva não pode ser negativo.")
        exit()

    return nome, cidade, temp, chance_cv, volume_cv


def avaliar_alagamento(chance_cv, volume_cv):
    """Retorna os status de alagamento e energia conforme os dados de chuva."""
    if chance_cv >= LIMITE_CHANCE_ALTA and volume_cv >= LIMITE_VOLUME_CRITICO:
        alagamento = "Alerta VERMELHO: Risco ALTO de alagamento e volume crítico."
        energia    = "Possibilidade de queda de energia: ALTA."
    elif chance_cv >= LIMITE_CHANCE_MEDIA and volume_cv >= LIMITE_VOLUME_MEDIO:
        alagamento = "Alerta AMARELO: Risco moderado. Escoamento pode ficar lento."
        energia    = "Possibilidade de queda de energia: MÉDIA/BAIXA."
    elif chance_cv >= LIMITE_CHANCE_BAIXA:
        alagamento = "OBSERVAÇÃO: Chuva leve prevista. Sem grandes riscos."
        energia    = "Risco de queda de energia é MÍNIMO."
    else:
        alagamento = "Alerta VERDE: Pouca chance de chuva."
        energia    = "O risco de queda de energia é BAIXO/NULO."

    return alagamento, energia


def montar_mochila(temp, chance_cv):
    """Retorna a lista de itens recomendados para o clima atual."""
    itens = ["Carteira", "Celular"]

    if temp > TEMP_QUENTE:
        itens.extend(["Protetor Solar", "Garrafa de Água", "Boné"])
        if chance_cv < LIMITE_CHANCE_MEDIA:
            itens.append("Óculos de Sol")
    elif temp >= TEMP_AGRADAVEL:
        if chance_cv < LIMITE_CHANCE_MEDIA:
            itens.append("Óculos de Sol")
    else:
        itens.append("Casaco")

    if chance_cv >= LIMITE_CHANCE_MEDIA:
        itens.append("Guarda-chuva ou Capa")

    return list(dict.fromkeys(itens))  # remove duplicatas 


def gerar_msg_clima(temp):
    """Retorna a mensagem descritiva do clima pela temperatura."""
    if temp > TEMP_QUENTE:
        return "Você deve usar protetor solar!"
    elif temp >= TEMP_AGRADAVEL:
        return "O clima está agradável hoje."
    else:
        return "Hoje está muito frio!"


def exibir_relatorio(nome, cidade, temp, chance_cv, volume_cv):
    """Monta e imprime o relatório final."""
    msg_clima           = gerar_msg_clima(temp)
    status_alag, status_en = avaliar_alagamento(chance_cv, volume_cv)
    itens               = montar_mochila(temp, chance_cv)

    print("\n" + "=" * 80)
    print(f"  Olá, {nome}! Relatório climático para {cidade}")
    print("=" * 80)
    print(f"   Temperatura       : {temp}°C — {msg_clima}")
    print(f"   Chance de chuva   : {chance_cv}%")
    print(f"   Volume previsto   : {volume_cv} mm")   
    print(f"   Alagamento        : {status_alag}")
    print(f"   Energia           : {status_en}")
    print("-" * 80)
    print(f"   Leve na mochila   : {', '.join(itens)}")
    print("=" * 80)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
nome, cidade, temp, chance_cv, volume_cv = coletar_dados()
exibir_relatorio(nome, cidade, temp, chance_cv, volume_cv)