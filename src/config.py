#Configurações compartilhadas entre as camadas: caminhos, colunas e regras de padronização

from pathlib import Path

# Caminhos absolutos a partir da raiz do projeto: funciona de qualquer pasta onde o comando for rodado
RAIZ = Path(__file__).resolve().parent.parent
BRONZE = RAIZ / "dados" / "bronze" / "pedidos_metalurgica_mezzalira.xlsx"
PRATA = RAIZ / "dados" / "prata" / "pedidos_prata.csv"
LOG = RAIZ / "dados" / "prata" / "log.csv"
OURO = RAIZ / "dados" / "ouro" / "faturamento_cidade_mes.csv"
PLANILHA_SHEETS = RAIZ / "saida" / "mezzalira_para_sheets.xlsx"

COLUNAS = ["Pedido", "Data", "Cliente", "Cidade", "Produto", "Valor (R$)"]
COLUNAS_LOG = ["O que encontrei", "O que fiz", "Linhas afetadas (na aba Bronze)", "Justificativa (se houve dúvida)",
              "Linhas restantes após a etapa"]

# De-para explícito: "REC" -> "Recife" não sairia de nenhuma regra de capitalização.
DE_PARA_CIDADES = {
    "recife": "Recife", "rec": "Recife", "olinda": "Olinda", "caruaru": "Caruaru",
    "petrolina": "Petrolina", "jaboatão dos guararapes": "Jaboatão dos Guararapes",
}
MESES = {"jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06",
         "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"}


def brl(x: float) -> str:
    #1234.5 -> 'R$ 1.234,50'
    return "R$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
