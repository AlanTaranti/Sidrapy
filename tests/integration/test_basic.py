import os

import requests

import sidrapy
import sidrapy.server



def test_ping():
    aux = sidrapy.server.ping()
    assert isinstance(aux, float)
    assert aux > 0
    assert aux < 10_000


def test_sample_request():
    # api docs here: http://api.sidra.ibge.gov.br/home/ajuda
    url = sidrapy.server.create_url(
        '/values/t/1612/p/2018/v/allxp/n1/1/d/m/h/y'
    )
    r = requests.get(url, timeout=10)
    assert r.status_code == 200
    sample_response = (
        '[\r\n  {\r\n    "NC": "Nível Territorial (Código)",\r\n    "NN": '
        '"Nível Territorial",\r\n    "D1C": "Ano (Código)",\r\n    "D1N": '
        '"Ano",\r\n    "D2C": "Variável (Código)",\r\n    "D2N": "Variável'
        '",\r\n    "D3C": "Brasil (Código)",\r\n    "D3N": "Brasil",\r\n  '
        '  "D4C": "Produto das lavouras temporárias (Código)",\r\n    "D4N":'
        ' "Produto das lavouras temporárias",\r\n    "MC": "Unidade de Medi'
        'da (Código)",\r\n    "MN": "Unidade de Medida",\r\n    "V": "Valo'
        'r"\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "NN": "Brasil",\r\n   '
        ' "D1C": "2018",\r\n    "D1N": "2018",\r\n    "D2C": "109",\r\n    '
        '"D2N": "Área plantada",\r\n    "D3C": "1",\r\n    "D3N": "Brasil"'
        ',\r\n    "D4C": "0",\r\n    "D4N": "Total",\r\n    "MC": "1006",'
        '\r\n    "MN": "Hectares",\r\n    "V": "73230674"\r\n  },\r\n  {\r\n'
        '    "NC": "1",\r\n    "NN": "Brasil",\r\n    "D1C": "2018",\r\n    '
        '"D1N": "2018",\r\n    "D2C": "216",\r\n    "D2N": "Área colhida",'
        '\r\n    "D3C": "1",\r\n    "D3N": "Brasil",\r\n    "D4C": "0",\r\n'
        '    "D4N": "Total",\r\n    "MC": "1006",\r\n    "MN": "Hectares",'
        '\r\n    "V": "72572833"\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "'
        'NN": "Brasil",\r\n    "D1C": "2018",\r\n    "D1N": "2018",\r\n   '
        ' "D2C": "214",\r\n    "D2N": "Quantidade produzida",\r\n    "D3C"'
        ': "1",\r\n    "D3N": "Brasil",\r\n    "D4C": "0",\r\n    "D4N": "'
        'Total",\r\n    "MC": "1017",\r\n    "MN": "Toneladas",\r\n    "V"'
        ': ".."\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "NN": "Brasil",\r\n'
        '    "D1C": "2018",\r\n    "D1N": "2018",\r\n    "D2C": "112",\r\n '
        '   "D2N": "Rendimento médio da produção",\r\n    "D3C": "1",\r\n '
        '   "D3N": "Brasil",\r\n    "D4C": "0",\r\n    "D4N": "Total",\r\n'
        '    "MC": "33",\r\n    "MN": "Quilogramas por Hectare",\r\n    "V'
        '": ".."\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "NN": "Brasil",\r\n'
        '    "D1C": "2018",\r\n    "D1N": "2018",\r\n    "D2C": "215",\r\n'
        '    "D2N": "Valor da produção",\r\n    "D3C": "1",\r\n    "D3N": '
        '"Brasil",\r\n    "D4C": "0",\r\n    "D4N": "Total",\r\n    "MC": '
        '"40",\r\n    "MN": "Mil Reais",\r\n    "V": "282971642"\r\n  }\r\n]'
    )
    assert r.text == sample_response


def test_server_get():
    path = "/values/t/1612/p/2018/v/allxp/n1/1/d/m/h/y"
    expected_response = (
        '[\r\n  {\r\n    "NC": "Nível Territorial (Código)",\r\n    "NN": '
        '"Nível Territorial",\r\n    "D1C": "Ano (Código)",\r\n    "D1N": '
        '"Ano",\r\n    "D2C": "Variável (Código)",\r\n    "D2N": "Variável'
        '",\r\n    "D3C": "Brasil (Código)",\r\n    "D3N": "Brasil",\r\n  '
        '  "D4C": "Produto das lavouras temporárias (Código)",\r\n    "D4N":'
        ' "Produto das lavouras temporárias",\r\n    "MC": "Unidade de Medi'
        'da (Código)",\r\n    "MN": "Unidade de Medida",\r\n    "V": "Valo'
        'r"\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "NN": "Brasil",\r\n   '
        ' "D1C": "2018",\r\n    "D1N": "2018",\r\n    "D2C": "109",\r\n    '
        '"D2N": "Área plantada",\r\n    "D3C": "1",\r\n    "D3N": "Brasil"'
        ',\r\n    "D4C": "0",\r\n    "D4N": "Total",\r\n    "MC": "1006",'
        '\r\n    "MN": "Hectares",\r\n    "V": "73230674"\r\n  },\r\n  {\r\n'
        '    "NC": "1",\r\n    "NN": "Brasil",\r\n    "D1C": "2018",\r\n    '
        '"D1N": "2018",\r\n    "D2C": "216",\r\n    "D2N": "Área colhida",'
        '\r\n    "D3C": "1",\r\n    "D3N": "Brasil",\r\n    "D4C": "0",\r\n'
        '    "D4N": "Total",\r\n    "MC": "1006",\r\n    "MN": "Hectares",'
        '\r\n    "V": "72572833"\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "'
        'NN": "Brasil",\r\n    "D1C": "2018",\r\n    "D1N": "2018",\r\n   '
        ' "D2C": "214",\r\n    "D2N": "Quantidade produzida",\r\n    "D3C"'
        ': "1",\r\n    "D3N": "Brasil",\r\n    "D4C": "0",\r\n    "D4N": "'
        'Total",\r\n    "MC": "1017",\r\n    "MN": "Toneladas",\r\n    "V"'
        ': ".."\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "NN": "Brasil",\r\n'
        '    "D1C": "2018",\r\n    "D1N": "2018",\r\n    "D2C": "112",\r\n '
        '   "D2N": "Rendimento médio da produção",\r\n    "D3C": "1",\r\n '
        '   "D3N": "Brasil",\r\n    "D4C": "0",\r\n    "D4N": "Total",\r\n'
        '    "MC": "33",\r\n    "MN": "Quilogramas por Hectare",\r\n    "V'
        '": ".."\r\n  },\r\n  {\r\n    "NC": "1",\r\n    "NN": "Brasil",\r\n'
        '    "D1C": "2018",\r\n    "D1N": "2018",\r\n    "D2C": "215",\r\n'
        '    "D2N": "Valor da produção",\r\n    "D3C": "1",\r\n    "D3N": '
        '"Brasil",\r\n    "D4C": "0",\r\n    "D4N": "Total",\r\n    "MC": '
        '"40",\r\n    "MN": "Mil Reais",\r\n    "V": "282971642"\r\n  }\r\n]'
    )
    response = sidrapy.server.get(path)
    assert response == expected_response


def test_table_metadata():
    code = 1612
    table = sidrapy.Table(code)
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, '../expected_raw_1612.txt')) as f:
        expected = f.read()
    raw = table.metadata.raw
    assert raw == expected
