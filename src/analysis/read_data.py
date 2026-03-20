import pandas as pd

print("RODANDO SCRIPT NOVO")

# =========================
# 1. LEITURA DOS DADOS
# =========================

sales = pd.read_csv("data/raw/vendas_2023_2024.csv")
products = pd.read_csv("data/raw/produtos_raw.csv")
customers = pd.read_json("data/raw/clientes_crm.json")
financials = pd.read_json("data/raw/custos_importacao.json")

# =========================
# 2. LIMPEZA DE DADOS
# =========================

# ---- SALES ----
sales["sale_date"] = pd.to_datetime(sales["sale_date"], errors="coerce")

# ---- PRODUCTS ----

# Corrigir preço (remover R$)
products["price"] = products["price"].str.replace("R$", "", regex=False)
products["price"] = products["price"].astype(float)

# Função para padronizar categorias
def clean_category(cat):
    cat = str(cat).upper()

    if "ELETR" in cat:
        return "ELETRONICOS"
    elif "PROP" in cat:
        return "PROPULSAO"
    elif "ANCOR" in cat or "ENCOR" in cat:
        return "ANCORAGEM"
    else:
        return "OUTROS"

# Aplicar limpeza
products["actual_category"] = products["actual_category"].apply(clean_category)

# =========================
# 3. VERIFICAÇÃO
# =========================

print("\nSALES:")
print(sales.head())

print("\nPRODUCTS:")
print(products.head())

print("\nCATEGORIAS PADRONIZADAS:")
print(products["actual_category"].unique())

print("\nTIPOS DE DADOS (SALES):")
print(sales.dtypes)

print("\nTIPOS DE DADOS (PRODUCTS):")
print(products.dtypes)

# =========================
# 4. SALVAR DADOS TRATADOS
# =========================

sales.to_csv("data/processed/sales_clean.csv", index=False)
products.to_csv("data/processed/products_clean.csv", index=False)

print("\nDADOS SALVOS EM data/processed/")