"""Testes do pipeline. Rodar da raiz do projeto com: pytest -v"""

import pandas as pd
import pytest

from src.ouro import faturamento_cidade_mes
from src.prata import converter_data, converter_valor, ler_bronze, transformar


def test_converter_valor():
    assert converter_valor(3260) == 3260.0
    assert converter_valor("R$ 1.200,00") == 1200.0
    assert converter_valor("R$ 630,00") == 630.0


def test_converter_data():
    assert converter_data("2026-03-05") == pd.Timestamp(2026, 3, 5)  # 5 de março, nunca 3 de maio
    assert converter_data("01-fev-2026") == pd.Timestamp(2026, 2, 1)
    with pytest.raises(ValueError):
        converter_data("31-fev-2026")  # data impossível tem que dar erro


def test_prata_com_planilha_real():
    bronze = ler_bronze()
    prata, _ = transformar(bronze)
    assert len(bronze) == 60 and len(prata) == 53
    assert set(prata["Cidade"]) == {"Recife", "Olinda", "Caruaru", "Petrolina", "Jaboatão dos Guararapes"}
    pd.testing.assert_frame_equal(bronze, ler_bronze())  # a Bronze continua intacta


def test_ouro_bate_com_prata():
    prata, _ = transformar(ler_bronze())
    assert faturamento_cidade_mes(prata).loc["Total", "Total"] == pytest.approx(prata["Valor (R$)"].sum())
