import pandas as pd
from pathlib import Path

DATA = Path("data")
src = DATA / "NOX-2020.csv"
dst = DATA / "nox.csv"

use_cols = ["Date.Local", "Time.Local", "Sample.Measurement"]
chunks = pd.read_csv(src, usecols=use_cols, dtype=str, chunksize=250_000)
first = True
for ch in chunks:
    ch.to_csv(dst, index=False, mode="w" if first else "a")
    first = False

print("OK -> data/nox.csv creado con columnas:", use_cols)
