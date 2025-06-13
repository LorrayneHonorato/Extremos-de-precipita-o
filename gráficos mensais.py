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

# Conversão de kg/m²/s para mm/dia
CONVERSAO_POR_SEGUNDO_PARA_MM_DIA = 86400

# Abrir o arquivo
with h5py.File(caminho, "r") as f:
    datas_raw = f["time"][:]
    datas = [datetime.strptime(str(int(d)), "%Y%m%d") for d in datas_raw]
    datas_np = np.array(datas)

    # Máscara para o período 1997–2024
    mascara = (datas_np >= datetime(1997, 1, 1)) & (datas_np <= datetime(2024, 12, 31))
    datas_filtradas = datas_np[mascara]

    # Inicializar dicionário para médias mensais
    medias_mensais = {var: np.zeros(12) for var in variaveis}

    for var in variaveis:
        dados = f[var][:][mascara]  # aplicar a máscara

        # Média espacial e vertical diária
        media_diaria = np.mean(dados, axis=(1, 2, 3, 4))

        # Conversão para mm/dia
        media_diaria_mm_dia = media_diaria * CONVERSAO_POR_SEGUNDO_PARA_MM_DIA

        # Agrupar por mês (1 a 12)
        soma_mensal = defaultdict(list)
        for valor, data in zip(media_diaria_mm_dia, datas_filtradas):
            soma_mensal[data.month].append(valor)

        # Calcular média do acumulado mensal
        for mes in range(1, 13):
            medias_mensais[var][mes - 1] = np.sum(soma_mensal[mes]) / len(soma_mensal[mes])  # média do acumulado

# Plot
meses_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
plt.figure(figsize=(12, 6))
for var in variaveis:
    plt.plot(meses_labels, medias_mensais[var], label=nomes_legenda[var], color=cores[var], marker='o')

plt.title("Média do Acumulado Mensal de Precipitação (1997–2024)")
plt.xlabel("Mês")
plt.ylabel("Média do Acumulado Mensal (mm)")
plt.legend(title="Variável")
plt.grid(True)
plt.tight_layout()
plt.show()
