#Camada Ouro: Prata -> Ouro

#Lê a Prata salva e calcula o faturamento por cidade × mês, que responde à pergunta da diretoria.
#Serve também de conferência independente da tabela dinâmica feita no Google Sheets.

import pandas as pd
from src.config import OURO, PRATA, brl

NOMES_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
               "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def ler_prata():
    return pd.read_csv(PRATA, parse_dates=["Data"])


def faturamento_cidade_mes(prata: pd.DataFrame):
    return prata.assign(Mês=prata["Data"].dt.strftime("%Y-%m")).pivot_table(
        index="Cidade", columns="Mês", values="Valor (R$)", aggfunc="sum", fill_value=0,
        margins=True, margins_name="Total")


def maior_faturamento(prata: pd.DataFrame):
    #Combinação cidade + mês com o maior faturamento
    total = prata.groupby(["Cidade", prata["Data"].dt.to_period("M")])["Valor (R$)"].sum()
    cidade, mes = total.idxmax()
    return cidade, mes, total.max()


def descrever(cidade: str, mes, valor: float):
    return f"{cidade}, em {NOMES_MESES[mes.month - 1]} de {mes.year} ({brl(valor)})"


def executar():
    prata = ler_prata()
    ouro = faturamento_cidade_mes(prata)
    OURO.parent.mkdir(parents=True, exist_ok=True)
    ouro.to_csv(OURO)
    print("[Ouro] Faturamento por cidade × mês (compare com a tabela dinâmica do Sheets):\n")
    print(ouro.map(brl).to_string(), "\n")
    print("[Ouro] Maior faturamento:", descrever(*maior_faturamento(prata)))


if __name__ == "__main__":
    executar()
