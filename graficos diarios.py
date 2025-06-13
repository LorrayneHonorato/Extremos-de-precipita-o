import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

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

def media_movel(data, janela=15):
    """Calcula média móvel simples com janela especificada."""
    return np.convolve(data, np.ones(janela)/janela, mode='same')

# Abrir o arquivo e processar os dados
with h5py.File(caminho, "r") as f:
    datas_raw = f["time"][:]
    datas = [datetime.strptime(str(int(d)), "%Y%m%d") for d in datas_raw]
    datas_np = np.array(datas)

    # Máscara para o período 1997–2024
    mascara = (datas_np >= datetime(1997, 1, 1)) & (datas_np <= datetime(2024, 12, 31))
    datas_filtradas = datas_np[mascara]

    plt.figure(figsize=(14, 7))

    for var in variaveis:
        dados = f[var][:][mascara]

        # Média espacial e vertical para cada dia
        media_diaria = np.mean(dados, axis=(1, 2, 3, 4))

        # Converter para mm/dia
        media_diaria_mm_dia = media_diaria * CONVERSAO_POR_SEGUNDO_PARA_MM_DIA

        # Suavizar com média móvel 15 dias
        media_suavizada = media_movel(media_diaria_mm_dia, janela=15)

        # Plotar série suavizada
        plt.plot(datas_filtradas, media_suavizada, label=nomes_legenda[var], color=cores[var])

    plt.title("Média do Acumulado Diário das Precipitações Suavizada (Janela 15 dias)\n(1997–2024)")
    plt.xlabel("Data")
    plt.ylabel("Média Diária Suavizada (mm/dia)")
    plt.legend(title="Variável")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
