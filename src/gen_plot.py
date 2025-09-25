import pandas as pd
import matplotlib.pyplot as plt

# Lee nox.csv (3 columnas: Date.Local, Time.Local, Sample.Measurement)
df = pd.read_csv("data/nox.csv", dtype=str)
df["ts"] = pd.to_datetime(
    df["Date.Local"].str.strip()+" "+df["Time.Local"].str.strip(),
    errors="coerce"
)
df["y"] = pd.to_numeric(df["Sample.Measurement"], errors="coerce")
df = df.dropna(subset=["ts","y"])

# (Opcional) Agregar por instante para suavizar y reducir tamaño
agg = df.groupby("ts", as_index=False)["y"].mean()

plt.figure(figsize=(12,5))
plt.plot(agg["ts"], agg["y"])
plt.title("TS-NOX-202")
plt.xlabel("Tiempo (Date.Local + Time.Local)")
plt.ylabel("Sample.Measurement")
plt.tight_layout()
plt.savefig("TS-NOX-202.png", dpi=150)
