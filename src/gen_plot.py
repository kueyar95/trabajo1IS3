import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/nox.csv", dtype=str)

ts = pd.to_datetime(df["Date.Local"].str.strip() + " " + df["Time.Local"].str.strip(), errors="coerce")
y  = pd.to_numeric(df["Sample.Measurement"], errors="coerce")

agg = pd.DataFrame({"ts": ts, "y": y}).dropna()
agg = agg.groupby("ts", as_index=False)["y"].mean()

plt.figure(figsize=(12,5))
plt.plot(agg["ts"], agg["y"])
plt.title("TS-NOX-202")
plt.xlabel("Tiempo (Date.Local + Time.Local)")
plt.ylabel("Sample.Measurement")
plt.tight_layout()
plt.savefig("TS-NOX-202.png", dpi=150)
print("OK -> TS-NOX-202.png")
