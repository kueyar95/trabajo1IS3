import sys
from pathlib import Path
import pandas as pd

DATA = Path("data")
EXT  = DATA / "NOX-2020-ext.csv"

# Salidas
NOX     = DATA / "NOX-2020.csv"
STATES  = DATA / "states.csv"
COUNTIES= DATA / "counties.csv"
METHODS = DATA / "methods.csv"

if not EXT.exists():
    print(f"[ERROR] No existe {EXT}. Genera primero NOX-2020-ext.csv y reintenta.", file=sys.stderr)
    sys.exit(1)

# Columnas esperadas, separador TAB, archivo potencialmente grande
usecols = ["State.Code","County.Code","Site.Num","Latitude","Longitude",
           "Date.Local","Time.Local","Sample.Measurement","Method.Type",
           "Method.Code","Method.Name","State.Name","County.Name"]

first = True
states_set, counties_set, methods_set = set(), set(), set()

# Leemos por chunks para no quedarnos sin RAM
for ch in pd.read_csv(EXT, sep="\t", usecols=usecols, dtype=str, chunksize=250_000):
    # Normaliza espacios y comillas residuales (por si vienen entrecomilladas)
    ch = ch.applymap(lambda s: s.strip().strip('"') if isinstance(s, str) else s)

    # 1) NOX-2020.csv = NOX-2020-ext.csv SIN State.Name, County.Name, Method.Name
    out = ch.drop(columns=["State.Name","County.Name","Method.Name"])
    out.to_csv(NOX, index=False, mode=("w" if first else "a"))
    first = False

    # 2) Catálogos únicos
    #    - states.csv: State.Code + State.Name
    states_set.update(
        ch[["State.Code","State.Name"]]
        .dropna()
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )

    #    - counties.csv: County.Code + County.Name  (según lo pedido)
    counties_set.update(
        ch[["County.Code","County.Name"]]
        .dropna()
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )

    #    - methods.csv: Method.Code + Method.Name
    methods_set.update(
        ch[["Method.Code","Method.Name"]]
        .dropna()
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )

# Volcamos catálogos ordenados
pd.DataFrame(sorted(states_set), columns=["State.Code","State.Name"]).to_csv(STATES, index=False)
pd.DataFrame(sorted(counties_set), columns=["County.Code","County.Name"]).to_csv(COUNTIES, index=False)
pd.DataFrame(sorted(methods_set), columns=["Method.Code","Method.Name"]).to_csv(METHODS, index=False)

# Conteos (los imprime para que compares con la pauta)
n_states  = sum(1 for _ in open(STATES))  - 1  # sin header
n_county  = sum(1 for _ in open(COUNTIES)) - 1
n_methods = sum(1 for _ in open(METHODS)) - 1
n_rows    = sum(1 for _ in open(NOX))      - 1

print("==== Resumen de verificación ====")
print(f"Estados únicos: {n_states}")
print(f"Condados únicos: {n_county}")
print(f"Métodos únicos: {n_methods}")
print(f"Registros NOX-2020.csv: {n_rows}")
print("Archivos generados en data/: NOX-2020.csv, states.csv, counties.csv, methods.csv")
