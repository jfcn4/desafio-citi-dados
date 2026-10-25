# Desafio CITi · Do dado bagunçado ao primeiro assistente

Pipeline em Python na arquitetura medalhão (Bronze -> Prata -> Ouro) para a planilha de
pedidos da Metalúrgica Mezzalira, e o assistente de manutenção feito no Gemini Gems.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python pipeline.py               # roda todas as camadas, em ordem
python -m src.prata              # ou uma camada de cada vez
pytest -v
```

## Estrutura

```
pipeline.py               orquestra as camadas, em ordem
src/
  config.py               caminhos, colunas e regras de padronização (de-para de cidades)
  prata.py                Bronze -> Prata: corrige os 5 problemas e gera o Log
  ouro.py                 Prata -> Ouro: faturamento por cidade × mês e a resposta
  exportar.py             monta o .xlsx (Bronze, Prata, Log) para o Google Sheets
tests/                    testes automatizados
dados/
  bronze/                 planilha original (nunca alterada)
  prata/                  gerado: pedidos limpos + log
  ouro/                   gerado: faturamento por cidade × mês
saida/                    gerado: planilha para importar no Google Sheets
etapa2_assistente/        instruções do Gem, tabela de testes, prints e material de apoio
```

As camadas conversam por **dado salvo**: a Prata grava `dados/prata/`, e a Ouro lê de lá.
Cada camada pode ser refeita sem rodar as outras.

## Decisões

| Decisão | Por quê |
|---|---|
| Bronze é uma cópia fiel do arquivo original | Dá para refazer tudo e auditar o antes e o depois |
| Padronizar antes de deduplicar | "recife" e "Recife" esconderiam uma cópia se a ordem fosse inversa |
| Cidades por tabela de-para | “REC” -> “Recife” não sairia de nenhuma regra de capitalização. |
| Conversões estritas | Valor ou data em formato inesperado dá erro em vez de passar em silêncio |
| Ouro em Python além da tabela dinâmica | Duas ferramentas independentes precisam chegar ao mesmo total |
