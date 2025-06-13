from netCDF4 import Dataset

# Caminho correto e nome exato do arquivo
caminho = r"C:\Users\lorra\OneDrive\Coisas antigas\Área de Trabalho\precipitacao_combinada.nc"

# Abre o arquivo NetCDF
ds = Dataset(caminho, 'r')

# Lista dimensões e variáveis
print("Dimensões:")
print(ds.dimensions.keys())

print("\nVariáveis:")
print(ds.variables.keys())

ds.close()



