from pathlib import Path

import nbformat as nbf
import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parent
np.random.seed(42)

lojas = {
    "Loja Centro": "Sudeste",
    "Loja Norte": "Norte",
    "Loja Sul": "Sul",
    "Loja Leste": "Nordeste",
}
produtos = {
    "Notebook": ("Eletronicos", 3500),
    "Smartphone": ("Eletronicos", 2200),
    "Teclado": ("Acessorios", 180),
    "Mouse": ("Acessorios", 120),
    "Cadeira": ("Moveis", 900),
    "Mesa": ("Moveis", 1250),
    "Monitor": ("Eletronicos", 1400),
    "Headset": ("Acessorios", 350),
}

datas = pd.date_range("2025-01-01", "2026-10-31", freq="D")
linhas = []
for data in datas:
    for _ in range(2):
        loja = np.random.choice(list(lojas))
        produto = np.random.choice(list(produtos))
        categoria, preco_base = produtos[produto]
        quantidade = int(np.random.choice([1, 2, 3, 4, 5], p=[0.35, 0.25, 0.2, 0.12, 0.08]))
        preco = round(preco_base * np.random.uniform(0.88, 1.12), 2)
        linhas.append({
            "data": data,
            "loja": loja,
            "produto": produto,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "regiao": lojas[loja],
            "categoria": categoria,
        })

df = pd.DataFrame(linhas)
for indice in np.random.choice(df.index, size=18, replace=False):
    df.loc[indice, "quantidade" if indice % 2 == 0 else "preco_unitario"] = np.nan
df.to_csv(BASE / "vendas.csv", index=False, date_format="%Y-%m-%d")

notebook = nbf.v4.new_notebook()

cells = []
cells.append(nbf.v4.new_markdown_cell(
    "# Painel de Analise de Vendas\n"
    "Notebook referente ao painel interativo de vendas do varejo."
))

cells.append(nbf.v4.new_code_cell(
    'import pandas as pd\n'
    'import numpy as np\n'
    'import matplotlib.pyplot as plt\n'
    'import seaborn as sns\n'
    '\n'
    'sns.set_style("whitegrid")\n'
    'sns.set_palette(sns.color_palette("deep"))\n'
    '%matplotlib inline'
))

cells.append(nbf.v4.new_markdown_cell(
    "## Etapa 1 - Preparacao e importacao\n"
    "Execute o arquivo `vendas.csv` junto a este notebook no Colab."
))

cells.append(nbf.v4.new_code_cell(
    'from pathlib import Path\n'
    '\n'
    'caminho_csv = Path("vendas.csv")\n'
    'if not caminho_csv.exists():\n'
    '    try:\n'
    '        from google.colab import files\n'
    '        print("Selecione o arquivo vendas.csv.")\n'
    '        enviado = files.upload()\n'
    '        caminho_csv = Path(next(iter(enviado)))\n'
    '    except ImportError:\n'
    '        raise FileNotFoundError("O arquivo vendas.csv nao foi encontrado.")\n'
    '\n'
    'df = pd.read_csv(caminho_csv)\n'
    'df["data"] = pd.to_datetime(df["data"], errors="coerce")\n'
    'df["faturamento"] = df["quantidade"] * df["preco_unitario"]\n'
    'df["mes"] = df["data"].dt.month\n'
    'df.head()'
))

cells.append(nbf.v4.new_code_cell(
    'print("Informacoes do dataset")\n'
    'df.info()\n'
    '\n'
    'print("\\nValores ausentes")\n'
    'print(df.isnull().sum())\n'
    '\n'
    'print("\\nResumo estatistico")\n'
    'display(df.describe(include="all"))'
))

cells.append(nbf.v4.new_code_cell(
    'df["quantidade"] = df["quantidade"].fillna(df["quantidade"].mean())\n'
    'df["preco_unitario"] = df["preco_unitario"].fillna(df["preco_unitario"].mean())\n'
    'df["faturamento"] = df["quantidade"] * df["preco_unitario"]\n'
    '\n'
    'print("Valores ausentes apos o tratamento:")\n'
    'print(df.isnull().sum())'
))

cells.append(nbf.v4.new_markdown_cell("## Etapa 2 - Analise exploratoria"))

cells.append(nbf.v4.new_code_cell(
    'faturamento_loja = df.groupby("loja", as_index=True)["faturamento"].sum().sort_values(ascending=False)\n'
    'print("Faturamento total por loja")\n'
    'display(faturamento_loja)'
))

cells.append(nbf.v4.new_code_cell(
    'ticket_medio = df.groupby("loja").agg(\n'
    '    faturamento_total=("faturamento", "sum"),\n'
    '    numero_vendas=("faturamento", "count")\n'
    ')\n'
    'ticket_medio["ticket_medio"] = ticket_medio["faturamento_total"] / ticket_medio["numero_vendas"]\n'
    'ticket_medio = ticket_medio.sort_values("ticket_medio", ascending=False)\n'
    'display(ticket_medio)'
))

cells.append(nbf.v4.new_code_cell(
    'cinco_mais_vendidos = df.groupby("produto", as_index=False)["quantidade"].sum().sort_values("quantidade", ascending=False).head(5)\n'
    'display(cinco_mais_vendidos)'
))

cells.append(nbf.v4.new_code_cell(
    'resumo_mensal = df.assign(mes_ano=df["data"].dt.to_period("M")).groupby("mes_ano")["faturamento"].sum()\n'
    'mes_maior = resumo_mensal.idxmax()\n'
    'mes_menor = resumo_mensal.idxmin()\n'
    'print(f"Mes com maior faturamento: {mes_maior.strftime(\'%m/%Y\')} - R$ {resumo_mensal.max():,.2f}")\n'
    'print(f"Mes com menor faturamento: {mes_menor.strftime(\'%m/%Y\')} - R$ {resumo_mensal.min():,.2f}")'
))

cells.append(nbf.v4.new_markdown_cell("## Etapa 3 - Visualizacoes"))

cells.append(nbf.v4.new_code_cell(
    'Path("graficos").mkdir(exist_ok=True)\n'
    '\n'
    'cores = sns.color_palette("deep", n_colors=len(faturamento_loja))\n'
    'ax = faturamento_loja.plot(kind="bar", color=cores, figsize=(10, 6))\n'
    'ax.set_title("Faturamento Total por Loja")\n'
    'ax.set_xlabel("Loja")\n'
    'ax.set_ylabel("Faturamento (R$)")\n'
    'plt.xticks(rotation=30, ha="right")\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/faturamento_por_loja.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_code_cell(
    'plt.figure(figsize=(12, 6))\n'
    'ax = resumo_mensal.plot(marker="o", linewidth=2)\n'
    'ax.set_title("Evolucao Mensal do Faturamento")\n'
    'ax.set_xlabel("Mes/Ano")\n'
    'ax.set_ylabel("Faturamento (R$)")\n'
    'rotulos = [periodo.strftime("%m/%Y") for periodo in resumo_mensal.index]\n'
    'plt.xticks(range(len(rotulos)), rotulos, rotation=45)\n'
    'for x, valor in enumerate(resumo_mensal.values):\n'
    '    ax.annotate(f"R$ {valor:,.0f}", (x, valor), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/evolucao_mensal_faturamento.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_code_cell(
    'faturamento_regiao = df.groupby("regiao")["faturamento"].sum().sort_values(ascending=False)\n'
    'cores_pizza = sns.color_palette("deep", n_colors=len(faturamento_regiao))\n'
    'plt.figure(figsize=(9, 7))\n'
    'plt.pie(faturamento_regiao, labels=faturamento_regiao.index, autopct="%1.1f%%", startangle=90, colors=cores_pizza)\n'
    'plt.title("Distribuicao do Faturamento por Regiao")\n'
    'plt.axis("equal")\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/faturamento_por_regiao.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_code_cell(
    'plt.figure(figsize=(10, 6))\n'
    'sns.scatterplot(data=df, x="quantidade", y="faturamento", hue="loja", alpha=0.75)\n'
    'plt.title("Relacao entre Quantidade Vendida e Faturamento")\n'
    'plt.xlabel("Quantidade vendida")\n'
    'plt.ylabel("Faturamento (R$)")\n'
    'plt.legend(title="Loja", bbox_to_anchor=(1.02, 1), loc="upper left")\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/quantidade_vs_faturamento.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_code_cell(
    'plt.figure(figsize=(11, 7))\n'
    'sns.boxplot(data=df, x="categoria", y="preco_unitario", hue="categoria", palette="deep", legend=False)\n'
    'plt.title("Distribuicao dos Precos Unitarios por Categoria")\n'
    'plt.xlabel("Categoria")\n'
    'plt.ylabel("Preco unitario (R$)")\n'
    'plt.xticks(rotation=20)\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/precos_por_categoria.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_code_cell(
    'correlacao = df.select_dtypes(include=[np.number]).corr()\n'
    'plt.figure(figsize=(9, 7))\n'
    'sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, square=True)\n'
    'plt.title("Correlacao entre Variaveis Numericas")\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/heatmap_correlacao.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_markdown_cell("## Etapa 4 - Apresentacao consolidada"))

cells.append(nbf.v4.new_code_cell(
    'fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n'
    '\n'
    'faturamento_loja.plot(kind="bar", ax=axes[0], color=sns.color_palette("deep", n_colors=len(faturamento_loja)))\n'
    'axes[0].set_title("Faturamento por Loja")\n'
    'axes[0].set_xlabel("Loja")\n'
    'axes[0].set_ylabel("Faturamento (R$)")\n'
    'axes[0].tick_params(axis="x", rotation=25)\n'
    '\n'
    'axes[1].pie(faturamento_regiao, labels=faturamento_regiao.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("deep", n_colors=len(faturamento_regiao)))\n'
    'axes[1].set_title("Faturamento por Regiao")\n'
    'axes[1].axis("equal")\n'
    '\n'
    'plt.tight_layout()\n'
    'plt.savefig("graficos/comparativo_loja_regiao.png", dpi=150, bbox_inches="tight")\n'
    'plt.show()'
))

cells.append(nbf.v4.new_code_cell(
    'resumo_lojas = df.groupby("loja").agg(\n'
    '    faturamento_total=("faturamento", "sum"),\n'
    '    quantidade_vendida=("quantidade", "sum"),\n'
    '    numero_vendas=("faturamento", "count")\n'
    ').reset_index()\n'
    'resumo_lojas["ticket_medio"] = resumo_lojas["faturamento_total"] / resumo_lojas["numero_vendas"]\n'
    'resumo_lojas = resumo_lojas.sort_values("faturamento_total", ascending=False)\n'
    'resumo_lojas.to_csv("resumo_analitico.csv", index=False, encoding="utf-8-sig")\n'
    'display(resumo_lojas)'
))

cells.append(nbf.v4.new_markdown_cell(
    "## Observacoes finais\n"
    "- A maior concentracao de faturamento pode ser comparada diretamente no grafico por loja.\n"
    "- A evolucao mensal permite identificar crescimento, quedas e sazonalidade.\n"
    "- A participacao regional mostra quais mercados possuem maior representatividade.\n"
    "- O grafico de dispersao ajuda a observar a relacao entre volume vendido e faturamento, bem como possiveis valores extremos.\n"
    "- O boxplot revela categorias com maior variacao de preco unitario.\n"
    "- O heatmap resume correlacoes entre as variaveis numericas do conjunto de dados."
))

notebook["cells"] = cells
nbf.write(notebook, BASE / "painel_vendas.ipynb")
print(BASE / "painel_vendas.ipynb")
