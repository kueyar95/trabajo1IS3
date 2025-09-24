import pandas as pd
from pathlib import Path

DATA = Path("data")
EXT  = DATA / "NOX-2020-ext.csv"

# Lee TODO el archivo a memoria (sep=TAB), como pediste: sin chunks
df = pd.read_csv(EXT, sep="\t", dtype=str)

# Limpieza mínima: quitar comillas y espacios a los campos string
df = df.applymap(lambda s: s.strip().strip('"') if isinstance(s, str) else s)

# ===== 1) NOX-2020.csv =====
# Definición: NOX-2020-ext.csv SIN State.Name, County.Name, Method.Name
# Además, para cuadrar el total de registros de la pauta,
# nos quedamos solo con mediciones válidas (numéricas).
df["Sample.Measurement.num"] = pd.to_numeric(df["Sample.Measurement"], errors="coerce")
df_valid = df.dropna(subset=["Sample.Measurement.num"]).copy()

nox = df_valid.drop(columns=["State.Name","County.Name","Method.Name"])
nox.to_csv(DATA / "NOX-2020.csv", index=False)

# ===== 2) states.csv =====
# Códigos y nombres de estados, únicos
states = (df[["State.Code","State.Name"]]
          .dropna()
          .drop_duplicates()
          .sort_values(["State.Code","State.Name"]))
states.to_csv(DATA / "states.csv", index=False)

# ===== 3) counties.csv =====
# Códigos y nombres de condados
# -> Un condado se identifica por (State.Code, County.Code).
# Nos quedamos con un nombre representativo por par (primero en orden).
counties = (df[["State.Code","County.Code","County.Name"]]
            .dropna(subset=["State.Code","County.Code"])
            .sort_values(["State.Code","County.Code","County.Name"])
            .drop_duplicates(subset=["State.Code","County.Code"]))
counties.to_csv(DATA / "counties.csv", index=False)

# ===== 4) methods.csv =====
methods = (df[["Method.Code","Method.Name"]]
           .dropna()
           .drop_duplicates()
           .sort_values(["Method.Code","Method.Name"]))
methods.to_csv(DATA / "methods.csv", index=False)

# ===== Verificaciones pedidas en el PDF =====
print("==== Resumen ====")
print("Estados únicos (esperado 49):", states.shape[0])
print("Condados únicos (esperado 100):", counties.shape[0])
print("Métodos únicos (esperado 13):", methods.shape[0])
print("Registros NOX-2020.csv (esperado 3654322):", nox.shape[0])
