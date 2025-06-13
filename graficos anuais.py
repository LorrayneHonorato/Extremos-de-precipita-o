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

# Cores para cada variável
cores = {
    "PFICU": "tab:blue",
    "PFILSAN": "tab:green",
    "PFLCU": "tab:red",
    "PFLLSAN": "tab:orange"
}

# Fator de conversão de kg/m²/s para mm/dia
CONVERSAO_POR_SEGUNDO_PARA_MM_DIA = 86400

# Abrir o arquivo
with h5py.File(caminho, "r") as f:
    datas_raw = f["time"][:]
    datas = [datetime.strptime(str(int(d)), "%Y%m%d") for d in datas_raw]
    datas_np = np.array(datas)

    # Máscara para o período 1997–2024
    mascara = (datas_np >= datetime(1997, 1, 1)) & (datas_np <= datetime(2024, 12, 31))
    datas_filtradas = datas_np[mascara]

    # Inicializar dicionário com acumulados anuais
    acumulados = {}

    for var in variaveis:
        dados = f[var][:][mascara]  # aplicar máscara diretamente

        # Média espacial e vertical
        media_diaria = np.mean(dados, axis=(1, 2, 3, 4))

        # Converter de fluxo para mm/dia
        media_diaria_mm_dia = media_diaria * CONVERSAO_POR_SEGUNDO_PARA_MM_DIA

        # Agrupar por ano
        acumulado_anual = defaultdict(list)
        for valor, data in zip(media_diaria_mm_dia, datas_filtradas):
            acumulado_anual[data.year].append(valor)

        # Calcular soma anual
        anos = sorted(acumulado_anual.keys())
        soma_anual = [np.sum(acumulado_anual[ano]) for ano in anos]
        acumulados[var] = soma_anual

# Plot comparativo
plt.figure(figsize=(12, 6))
for var in variaveis:
    plt.plot(anos, acumulados[var], label=nomes_legenda[var], color=cores[var], marker='o')

plt.title("Comparativo Anual das Precipitações (1997–2024)")
plt.xlabel("Ano")
plt.ylabel("Acumulado Anual (mm)")
plt.legend(title="Variável")
plt.grid(True)
plt.tight_layout()
plt.show()
