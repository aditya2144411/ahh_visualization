import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_excel("C:/Users/ASUSX550I/Downloads/Book1.xlsx", skiprows=3)
df.columns = [
    "Provinsi", 
    "2023_L", "2022_L", "2021_L", "2020_L", 
    "2023_P", "2022_P", "2021_P", "2020_P"
]
replace_dict = {
    "DKI JAKARTA": "DAERAH KHUSUS IBUKOTA JAKARTA",
    "DI YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA",
    "KEP. RIAU": "RIAU",
    "KEP. BANGKA BELITUNG": "BANGKA BELITUNG",
    "NUSA TENGGARA BARAT": "NUSATENGGARA BARAT",
    "NUSA TENGGARA TIMUR": "NUSATENGGARA TIMUR",
    "RIAU'": "RIAU",
    "RIAL'": "RIAU",
    "PAPUA": "IRIAN JAYA TIMUR",
    "PAPUA BARAT": "IRIAN JAYA BARAT"
}

df_p = df[["Provinsi", "2023_P"]].copy()
df_p.columns = ["Provinsi", "AHH"]
df_p["Provinsi"] = df_p["Provinsi"].replace(replace_dict)

df_l = df[["Provinsi", "2023_L"]].copy()
df_l.columns = ["Provinsi", "AHH"]
df_l["Provinsi"] = df_l["Provinsi"].replace(replace_dict)

map_df = gpd.read_file("C:/Users/ASUSX550I/Downloads/indonesia_full.geojson")

merged_p = map_df.merge(df_p, left_on="Propinsi", right_on="Provinsi")
plt.figure(figsize=(12, 10))
merged_p.plot(column="AHH", cmap="YlGnBu", linewidth=0.8, edgecolor="black", legend=True)
plt.title("Peta AHH Perempuan Indonesia Tahun 2023", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig("peta_ahh_perempuan.png", dpi=300)
plt.show()

merged_l = map_df.merge(df_l, left_on="Propinsi", right_on="Provinsi")
plt.figure(figsize=(12, 10))
merged_l.plot(column="AHH", cmap="OrRd", linewidth=0.8, edgecolor="black", legend=True)
plt.title("Peta AHH Laki-laki Indonesia Tahun 2023", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig("peta_ahh_lakilaki.png", dpi=300)
plt.show()

df_gap = df_p.merge(df_l, on="Provinsi", suffixes=('_P', '_L'))
df_gap["Selisih"] = df_gap["AHH_P"] - df_gap["AHH_L"]

merged_gap = map_df.merge(df_gap, left_on="Propinsi", right_on="Provinsi")
plt.figure(figsize=(12, 10))
merged_gap.plot(column="Selisih", cmap="coolwarm", linewidth=0.8, edgecolor="black", legend=True)
plt.title("Peta Selisih AHH Perempuan - Laki-laki (2023)", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig("peta_selisih_ahh.png", dpi=300)
plt.show()

df_gap.to_excel("output_gap_ahh_2023.xlsx", index=False)

prov_tertinggi = df_p.sort_values(by="AHH", ascending=False).iloc[0]
prov_terendah = df_p.sort_values(by="AHH", ascending=True).iloc[0]
print(f"""
Kesimpulan:
- Provinsi dengan AHH perempuan tertinggi tahun 2023 adalah {prov_tertinggi['Provinsi']} dengan AHH {prov_tertinggi['AHH']:.2f}.
- Provinsi dengan AHH perempuan terendah adalah {prov_terendah['Provinsi']} dengan AHH {prov_terendah['AHH']:.2f}.
- Rata-rata selisih AHH perempuan-laki-laki di Indonesia tahun 2023 adalah {df_gap['Selisih'].mean():.2f} tahun.
""")

print(df_p["AHH"].describe())