#Camada Prata: Bronze -> Prata

#Lê a planilha original, corrige os 5 problemas na ordem certa e salva prata e o Log em dados/prata

import re
import pandas as pd
from src.config import BRONZE, COLUNAS, COLUNAS_LOG, DE_PARA_CIDADES, LOG, MESES, PRATA, brl


def ler_bronze():
    # dtype=object: le cada celula como está, sem adivinhar tipos
    return pd.read_excel(BRONZE, dtype=object)


def converter_valor(v):
    #3260 -> 3260.0 e 'R$ 1.200,00' -> 1200.0
    #tira o ponto de milhar antes de trocar a virgula
    if isinstance(v, str):
        v = v.replace("R$", "").strip().replace(".", "").replace(",", ".")
    return float(v)


def converter_data(v):
    #troca o mês abreviado por numero
    if not isinstance(v, str):
        return pd.Timestamp(v)
    v = v.strip().lower()
    for abrev, numero in MESES.items():
        v = v.replace(f"-{abrev}-", f"-{numero}-")
    formato = "%d-%m-%Y" if re.match(r"\d{1,2}-", v) else "%Y-%m-%d"
    return pd.to_datetime(v, format=formato)


def transformar(bronze: pd.DataFrame):
    df = bronze.copy()
    df["linha"] = df.index + 2  #o cabeçalho é a linha 1
    log = []

    def registrar(encontrei, fiz, mascara=None, justificativa="", remove=False):
        linhas = ", ".join(map(str, df.loc[mascara, "linha"])) if mascara is not None else "—"
        restantes = len(df) - (mascara.sum() if remove else 0)
        log.append([encontrei, fiz, linhas, justificativa, restantes])

    # 1. Linhas totalmente vazias
    vazia = df[COLUNAS].isna().all(axis=1)
    registrar(f"{vazia.sum()} linhas totalmente vazias", "Removi as linhas", vazia, remove=True)
    df = df[~vazia].copy()

    # 2. Cidades
    chave = df["Cidade"].str.strip().str.lower()
    for grafia in df.loc[df["Cidade"] != chave.map(DE_PARA_CIDADES), "Cidade"].unique():
        registrar(f'Cidade escrita como "{grafia}"', f'Padronizei para "{DE_PARA_CIDADES[grafia.strip().lower()]}"',
                  df["Cidade"] == grafia)
    df["Cidade"] = chave.map(DE_PARA_CIDADES)

    # 3. Valores digitados como texto
    texto = df["Valor (R$)"].map(lambda v: isinstance(v, str))
    registrar(f'{texto.sum()} valores digitados como texto (ex.: "R$ 1.200,00")',
              'Converti para número (tirei "R$" e o ponto de milhar, troquei a vírgula decimal por ponto)', texto)
    df["Valor (R$)"] = df["Valor (R$)"].map(converter_valor)

    # 4. Datas em texto (dois formatos diferentes)
    em_texto = df["Data"].map(lambda v: isinstance(v, str))
    abreviado = em_texto & df["Data"].astype(str).str.contains("[a-z]", case=False)
    registrar(f"{(em_texto & ~abreviado).sum()} datas em texto no formato AAAA-MM-DD", "Converti para data",
              em_texto & ~abreviado, "Formato ISO: não há ambiguidade entre dia e mês.")
    registrar(f"{abreviado.sum()} datas em texto com mês abreviado (ex.: 01-fev-2026)", "Converti para data",
              abreviado)
    df["Data"] = df["Data"].map(converter_data)

    # 5. Duplicatas: por ultimo, com tudo padronizado
    copia = df.duplicated(subset=COLUNAS)
    registrar(f"{copia.sum()} pedidos duplicados (linha inteira igual)", "Removi a cópia, mantive a 1ª ocorrência",
              copia, "Deduplicado depois de padronizar, para comparar linhas já limpas.", remove=True)
    df = df[~copia]

    # Verificações: se falharem, o caso exige decisão humana e o pipeline para
    if df[COLUNAS].isna().any().any():
        raise ValueError("Há células vazias ou não convertidas na Prata.")
    if df["Pedido"].duplicated().any():
        raise ValueError("Mesmo nº de pedido com conteúdo diferente: decidir manualmente.")
    registrar("Verificação: mesmo nº de pedido com conteúdo diferente", "Nenhum caso encontrado")

    registrar("Reconciliação",
              f"{len(bronze)} linhas na Bronze − {vazia.sum()} vazias − {copia.sum()} duplicadas = "
              f"{len(df)} na Prata. Faturamento total: {brl(df['Valor (R$)'].sum())}",
              justificativa="O total geral da tabela dinâmica (Ouro, no Sheets) tem que bater com este valor.")
    return df[COLUNAS].reset_index(drop=True), pd.DataFrame(log, columns=COLUNAS_LOG)


def executar():
    bronze = ler_bronze()
    prata, log = transformar(bronze)
    PRATA.parent.mkdir(parents=True, exist_ok=True)
    prata.to_csv(PRATA, index=False, date_format="%Y-%m-%d")
    log.to_csv(LOG, index=False)
    print(f"[Prata] {len(bronze)} linhas na Bronze -> {len(prata)} na Prata ({PRATA.relative_to(PRATA.parents[2])})")


if __name__ == "__main__":
    executar()
