# IMPORTS

from datetime import datetime

# CONSTANTES DE ALERTA

LIMITE_CHANCE_ALTA    = 80
LIMITE_VOLUME_CRITICO = 50
LIMITE_CHANCE_MEDIA   = 50
LIMITE_VOLUME_MEDIO   = 20
LIMITE_CHANCE_BAIXA   = 30
TEMP_QUENTE           = 30
TEMP_AGRADAVEL        = 20

# FUNÇÕES

def salvar_historico(nome, cidade, temp, chance_cv, volume_cv, status_alag, status_en, itens):
    """Salva o relatório num arquivo .txt com data e hora."""
    agora = datetime.now().strftime("%d/%m/%Y - %H:%M")  
    
    with open("historico_clima.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write("=" * 60 + "\n")
        arquivo.write(f"  Consulta em: {agora}\n")
        arquivo.write(f"  Usuario    : {nome}\n")          
        arquivo.write(f"  Cidade     : {cidade}\n")
        arquivo.write(f"  Temperatura: {temp}°C\n")
        arquivo.write(f"  Chuva      : {chance_cv}% | {volume_cv}mm\n")
        arquivo.write(f"  Alagamento : {status_alag}\n")
        arquivo.write(f"  Energia    : {status_en}\n")
        arquivo.write(f"  Mochila    : {', '.join(itens)}\n")
        arquivo.write("=" * 60 + "\n\n")
    
    print("\n Relatorio salvo em 'historico_clima.txt'!")


def coletar_numero(mensagem, tipo=float, minimo=None, maximo=None):
    """Fica perguntando até o usuário digitar um número válido."""
    while True:
        try:
            valor = tipo(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"[ERRO] O valor minimo e {minimo}. Tente novamente.")
            elif maximo is not None and valor > maximo:
                print(f"[ERRO] O valor maximo e {maximo}. Tente novamente.")
            else:
                return valor
        except ValueError:
            print("[ERRO] Digite apenas numeros. Tente novamente.")


def coletar_dados():
    """Coleta e valida todos os dados do usuário."""
    nome   = input("Qual o seu nome? ").strip().title()
    cidade = input("Qual o nome da sua cidade? ").strip().title()

    temp      = coletar_numero("Quantos graus esta fazendo agora? ", tipo=float, minimo=-20, maximo=60)
    chance_cv = coletar_numero("Qual a chance de chuva? (0 a 100): ", tipo=int, minimo=0, maximo=100)
    volume_cv = coletar_numero("Volume de chuva previsto em MM? ", tipo=float, minimo=0)

    return nome, cidade, temp, chance_cv, volume_cv


def avaliar_alagamento(chance_cv, volume_cv):
    """Retorna os status de alagamento e energia conforme os dados de chuva."""
    if chance_cv >= LIMITE_CHANCE_ALTA and volume_cv >= LIMITE_VOLUME_CRITICO:
        alagamento = "Alerta VERMELHO: Risco ALTO de alagamento e volume critico."
        energia    = "Possibilidade de queda de energia: ALTA."
    elif chance_cv >= LIMITE_CHANCE_MEDIA and volume_cv >= LIMITE_VOLUME_MEDIO:
        alagamento = "Alerta AMARELO: Risco moderado. Escoamento pode ficar lento."
        energia    = "Possibilidade de queda de energia: MEDIA/BAIXA."
    elif chance_cv >= LIMITE_CHANCE_BAIXA:
        alagamento = "OBSERVACAO: Chuva leve prevista. Sem grandes riscos."
        energia    = "Risco de queda de energia e MINIMO."
    else:
        alagamento = "Alerta VERDE: Pouca chance de chuva."
        energia    = "O risco de queda de energia e BAIXO/NULO."

    return alagamento, energia


def montar_mochila(temp, chance_cv):
    """Retorna a lista de itens recomendados para o clima atual."""
    itens = ["Carteira", "Celular"]

    if temp > TEMP_QUENTE:
        itens.extend(["Protetor Solar", "Garrafa de Agua", "Bone"])
        if chance_cv < LIMITE_CHANCE_MEDIA:
            itens.append("Oculos de Sol")
    elif temp >= TEMP_AGRADAVEL:
        if chance_cv < LIMITE_CHANCE_MEDIA:
            itens.append("Oculos de Sol")
    else:
        itens.append("Casaco")

    if chance_cv >= LIMITE_CHANCE_MEDIA:
        itens.append("Guarda-chuva ou Capa")

    return list(dict.fromkeys(itens))


def gerar_msg_clima(temp):
    """Retorna a mensagem descritiva do clima pela temperatura."""
    if temp > TEMP_QUENTE:
        return "Voce deve usar protetor solar!"
    elif temp >= TEMP_AGRADAVEL:
        return "O clima esta agradavel hoje."
    else:
        return "Hoje esta muito frio!"


def exibir_relatorio(nome, cidade, temp, chance_cv, volume_cv):
    """Monta e imprime o relatório final."""
    msg_clima              = gerar_msg_clima(temp)
    status_alag, status_en = avaliar_alagamento(chance_cv, volume_cv)
    itens                  = montar_mochila(temp, chance_cv)

    print("\n" + "=" * 80)
    print(f"  Ola, {nome}! Relatorio climatico para {cidade}")
    print("=" * 80)
    print(f"   Temperatura     : {temp}C  {msg_clima}")
    print(f"   Chance de chuva : {chance_cv}%")
    print(f"   Volume previsto : {volume_cv} mm")
    print(f"   Alagamento      : {status_alag}")
    print(f"   Energia         : {status_en}")
    print("-" * 80)
    print(f"   Leve na mochila : {', '.join(itens)}")
    print("=" * 80)

    return status_alag, status_en, itens  

# Execução 

nome, cidade, temp, chance_cv, volume_cv = coletar_dados()
status_alag, status_en, itens = exibir_relatorio(nome, cidade, temp, chance_cv, volume_cv)
salvar_historico(nome, cidade, temp, chance_cv, volume_cv, status_alag, status_en, itens)
