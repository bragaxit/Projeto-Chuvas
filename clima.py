# IMPORTAÇÃO

from datetime import datetime

# CONSTANTES DE ALERTA

LIMITE_CHANCE_ALTA    = 70
LIMITE_VOLUME_CRITICO = 50
LIMITE_CHANCE_MEDIA   = 50
LIMITE_VOLUME_MEDIO   = 20
LIMITE_CHANCE_BAIXA   = 30
TEMP_QUENTE           = 33
TEMP_AGRADAVEL        = 20

#VALIDAÇÃO DE NÚMEROS

def coletar_numero(mensagem, tipo=float, minimo=None, maximo=None):
    """Garante que o usuário digite um número válido dentro de um limite."""
    while True:
        try:
            valor = tipo(input(mensagem))
            if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
                print(f"[ERRO] O valor deve estar entre {minimo} e {maximo}.")
                continue
            return valor
        except ValueError:
            print("[ERRO] Por favor, digite apenas números.")
            
#MENSAGEM DE CLIMA

def gerar_msg_clima(temp):
    
    if temp > TEMP_QUENTE:
        return "Calor intenso! Use protetor solar."
    elif temp >= TEMP_AGRADAVEL:
        return "O clima está agradável."
    else:
        return "Está frio, agasalhe-se!"

# ALAGAMENTO E ENERGIA

def avaliar_alagamento(chance_cv, volume_cv):
    """Analisa o risco de alagamento e queda de energia."""
    if chance_cv >= LIMITE_CHANCE_ALTA and volume_cv >= LIMITE_VOLUME_CRITICO:
        return "Risco ALTO de alagamento!", "Possibilidade de queda: ALTA"
    elif chance_cv >= LIMITE_CHANCE_MEDIA and volume_cv >= LIMITE_VOLUME_MEDIO:
        return "Risco Moderado.", "Possibilidade de queda: MÉDIA"
    elif chance_cv >= LIMITE_CHANCE_BAIXA:
        return "Risco Baixo.", "Risco de queda: MÍNIMO"
    else:
        return "Sem riscos detectados.", "Risco de queda: NULO"

#MONTAGEM DA MOCHILA

def montar_mochila(temp, chance_cv):
    """Define itens essenciais para levar na mochila."""
    itens = ["Carteira", "Celular"]
    
    if temp > TEMP_QUENTE:
        itens.extend(["Garrafa d'Água", "Protetor Solar"])
    elif temp < TEMP_AGRADAVEL:
        itens.append("Casaco")
        
    if chance_cv >= LIMITE_CHANCE_MEDIA:
        itens.append("Guarda-chuva")
        
    return list(dict.fromkeys(itens)) # Remove duplicatas caso existam

#COLETA DE DADOS

def coletar_dados():
    """Pergunta os dados ao usuário e guarda tudo em um Dicionário."""
    print("--- INFORME OS DADOS ATUAIS ---")
    nome   = input("Seu nome: ").strip().title()
    cidade = input("Cidade: ").strip().title()
    

    temp   = coletar_numero("Temperatura atual (°C): ", float, -20, 60)
    chance = coletar_numero("Chance de chuva (0-100%): ", int, 0, 100)
    volume = coletar_numero("Volume de chuva (mm): ", float, 0, 500)
    
    return {
        "usuario": nome,
        "cidade": cidade,
        "temp": temp,
        "chance": chance,
        "volume": volume
    }

# RELATÓRIO

def processar_relatorio(dados):
    """Calcula os alertas e exibe o resumo na tela."""
    alag, energ = avaliar_alagamento(dados['chance'], dados['volume'])
    lista_mochila = montar_mochila(dados['temp'], dados['chance'])
    msg_temp = gerar_msg_clima(dados['temp'])
    
    dados.update({
        "alagamento": alag,
        "energia": energ,
        "mochila": lista_mochila,
        "mensagem": msg_temp,
        "data_hora": datetime.now().strftime("%d/%m/%Y - %H:%M")
    })
    
    # Exibição
    print("\n" + "="*60)
    print(f"   RELATÓRIO CLIMÁTICO - {dados['cidade'].upper()}")
    print("="*60)
    print(f"   Usuário     : {dados['usuario']}")
    print(f"   Clima       : {dados['temp']}°C ({dados['mensagem']})")
    print(f"   Chuva       : {dados['chance']}% com {dados['volume']}mm")
    print(f"   Alagamento  : {dados['alagamento']}")
    print(f"   Energia     : {dados['energia']}")
    print(f"   Na Mochila  : {', '.join(dados['mochila'])}")
    print("="*50)
    
    return dados

# SALVAR HISTÓRICO

def salvar_historico(dados):
    """Salva os dados de forma organizada no arquivo txt."""
    with open("historico_clima.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Registro em: {dados['data_hora']}\n")
        
        for chave, valor in dados.items():
            if chave != "data_hora":
                
                v_texto = ", ".join(valor) if isinstance(valor, list) else valor
                arquivo.write(f"{chave.capitalize():<12}: {v_texto}\n")
                
        arquivo.write("-" * 40 + "\n\n")
    
    print(f"Histórico atualizado em 'historico_clima.txt'!")

# EXECUÇÃO DO PROGRAMA

if __name__ == "__main__":
    # 1. Coleta os dados
    meus_dados = coletar_dados()
    
    # 2. Processa as informações e mostra o relatório
    meus_dados_completos = processar_relatorio(meus_dados)
    
    salvar_historico(meus_dados_completos)
