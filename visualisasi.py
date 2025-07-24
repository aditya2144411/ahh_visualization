import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("ahh_data.xlsx", skiprows=3)

df.columns = [
    "Provinsi", 
    "2023_L", "2022_L", "2021_L", "2020_L", 
    "2023_P", "2022_P", "2021_P", "2020_P"
]

df_long = pd.melt(df, id_vars=["Provinsi"],
                  var_name="Tahun_JK", value_name="AHH")

df_long[['Tahun', 'JK']] = df_long['Tahun_JK'].str.split("_", expand=True)
df_long['Tahun'] = df_long['Tahun'].astype(int)

sns.set(style="whitegrid")
plt.figure(figsize=(14, 6))
sns.lineplot(data=df_long, x="Tahun", y="AHH", hue="JK", style="Provinsi", markers=True)

plt.title("Tren Angka Harapan Hidup (AHH) per Provinsi dan Jenis Kelamin")
plt.xlabel("Tahun")
plt.ylabel("Angka Harapan Hidup")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

df_2023_p = df_long[(df_long['Tahun'] == 2023) & (df_long['JK'] == 'P')]
df_2023_p_sorted = df_2023_p.sort_values(by='AHH', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_2023_p_sorted, x="AHH", y="Provinsi", hue="Provinsi", palette="flare", legend=False)

plt.title("Top 10 Provinsi dengan AHH Perempuan Tertinggi Tahun 2023")
plt.xlabel("Angka Harapan Hidup")
plt.ylabel("Provinsi")
plt.tight_layout()
plt.show()

df_2023_l = df_long[(df_long['Tahun'] == 2023) & (df_long['JK'] == 'L')]
df_2023_l_sorted = df_2023_l.sort_values(by='AHH', ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_2023_l_sorted, x="AHH", y="Provinsi", hue="Provinsi", palette="crest", legend=False)

plt.title("Top 10 Provinsi dengan AHH Laki-laki Tertinggi Tahun 2023")
plt.xlabel("Angka Harapan Hidup")
plt.ylabel("Provinsi")
plt.tight_layout()
plt.show()

df_2023 = df_long[df_long["Tahun"] == 2023]
df_pivot = df_2023.pivot(index="Provinsi", columns="JK", values="AHH").reset_index()
df_pivot = df_pivot.sort_values(by="P", ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(data=df_pivot, x="L", y="Provinsi", color="skyblue", label="Laki-laki")
sns.barplot(data=df_pivot, x="P", y="Provinsi", color="salmon", alpha=0.7, label="Perempuan")

plt.title("Perbandingan AHH Laki-laki vs Perempuan per Provinsi (2023)")
plt.xlabel("Angka Harapan Hidup")
plt.ylabel("Provinsi")
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()

df_p = df_long[df_long['JK'] == 'P']
heatmap_data = df_p.pivot(index='Provinsi', columns='Tahun', values='AHH')

plt.figure(figsize=(12, 12))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", linewidths=0.5, fmt=".2f")

plt.title("Heatmap AHH Perempuan per Provinsi (2020–2023)")
plt.xlabel("Tahun")
plt.ylabel("Provinsi")
plt.tight_layout()
plt.show()

df_l = df_long[df_long['JK'] == 'L']
heatmap_l = df_l.pivot(index='Provinsi', columns='Tahun', values='AHH')

plt.figure(figsize=(12, 12))
sns.heatmap(heatmap_l, annot=True, cmap="OrRd", linewidths=0.5, fmt=".2f")

plt.title("Heatmap AHH Laki-laki per Provinsi (2020–2023)")
plt.xlabel("Tahun")
plt.ylabel("Provinsi")
plt.tight_layout()
plt.show()

pivot_p = df_long[df_long['JK'] == 'P'].pivot(index='Provinsi', columns='Tahun', values='AHH')
pivot_l = df_long[df_long['JK'] == 'L'].pivot(index='Provinsi', columns='Tahun', values='AHH')
gap_ahh = pivot_p - pivot_l

plt.figure(figsize=(12, 12))
sns.heatmap(gap_ahh, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")

plt.title("Gap AHH Perempuan - Laki-laki per Provinsi (2020–2023)")
plt.xlabel("Tahun")
plt.ylabel("Provinsi")
plt.tight_layout()
plt.show()