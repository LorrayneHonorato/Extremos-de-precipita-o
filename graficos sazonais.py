import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Caminho do arquivo
caminho = r"C:\Users\lorra\Downloads\download-20250612T230437Z-1-001\combinado.h5"

# Lista de variáveis
variaveis = ["PFICU", "PFILSAN", "PFLCU", "PFLLSAN"]
nomes_legenda = {
    "PFICU": "Convectiva Gelo",
    "PFILSAN": "Não Convectiva Gelo",
    "PFLCU": "Convectiva Líquida",
    "PFLLSAN": "Não Convectiva Líquida"
}
cores = {
    "PFICU": "tab:blue",
    "PFILSAN": "tab:green",
    "PFLCU": "tab:red",
    "PFLLSAN": "tab:orange"
}

# Conversão de kg/m²/s para mm/dia
CONVERSAO_POR_SEGUNDO_PARA_MM_DIA = 86400

# Definições sazonais
def estacao_do_ano(mes):
    if mes in [12, 1, 2]:
        return "Verão"
    elif mes in [3, 4, 5]:
        return "Outono"
    elif mes in [6, 7, 8]:
        return "Inverno"
    elif mes in [9, 10, 11]:
        return "Primavera"

# Abrir o arquivo
with h5py.File(caminho, "r") as f:
    datas_raw = f["time"][:]
    datas = [datetime.strptime(str(int(d)), "%Y%m%d") for d in datas_raw]
    datas_np = np.array(datas)

    # Máscara para o período 1997–2024
    mascara = (datas_np >= datetime(1997, 1, 1)) & (datas_np <= datetime(2024, 12, 31))
    datas_filtradas = datas_np[mascara]

    # Inicializar estrutura para armazenar dados por estação
    acumulado_sazonal = {var: defaultdict(list) for var in variaveis}

    for var in variaveis:
        dados = f[var][:][mascara]

        # Média espacial/vertical
        media_diaria = np.mean(dados, axis=(1, 2, 3, 4))

        # Converter para mm/dia
        media_diaria_mm_dia = media_diaria * CONVERSAO_POR_SEGUNDO_PARA_MM_DIA

        # Agrupar por estação
        for valor, data in zip(media_diaria_mm_dia, datas_filtradas):
            estacao = estacao_do_ano(data.month)
            acumulado_sazonal[var][estacao].append(valor)

# Calcular média do acumulado sazonal
ordem_estacoes = ["Verão", "Outono", "Inverno", "Primavera"]
sazonal_medias = {var: [np.sum(acumulado_sazonal[var][est]) / len(acumulado_sazonal[var][est]) for est in ordem_estacoes] for var in variaveis}

# Plot
plt.figure(figsize=(10, 6))
for var in variaveis:
    plt.plot(ordem_estacoes, sazonal_medias[var], label=nomes_legenda[var], color=cores[var], marker='o')

plt.title("Média do Acumulado Sazonal de Precipitação (1997–2024)")
plt.xlabel("Estação do Ano")
plt.ylabel("Média do Acumulado Sazonal (mm)")
plt.legend(title="Variável")
plt.grid(True)
plt.tight_layout()
plt.show()
