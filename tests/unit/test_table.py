import os
import uuid
from unittest.mock import Mock, patch

import pytest

import sidrapy


def test_table_class_init():
    table = sidrapy.Table(code=1612)
    assert table.code == 1612
    for code in [None, '', 1.1, [1], {1}, {1: 1}]:
        with pytest.raises(TypeError):
            _ = sidrapy.Table(code=code)
    for code in [-1, -2, 0]:
        with pytest.raises(ValueError):
            _ = sidrapy.Table(code=code)


@pytest.fixture(scope='function')
def table1612():
    return sidrapy.Table(code=1612)


@pytest.fixture(scope='function')
def md1612():
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, 'sample_response_desc_1612.txt')) as f:
        sample_desc = f.read()
    with patch('sidrapy.server.get', return_value=sample_desc):
        md = sidrapy.table.Metadata(sidrapy.Table(code=1612))
        yield md


def test_table_class_str(table1612):
    assert str(table1612) == '<Table: 1612>'


def test_table_class_metadata(table1612):
    assert not hasattr(table1612, '_metadata')
    md = table1612.metadata
    assert md.table is table1612
    assert hasattr(table1612, '_metadata')
    md2 = table1612.metadata
    assert md2 == md


def test_metadata_init(table1612):
    md = sidrapy.table.Metadata(table1612)
    assert md.table == table1612.metadata.table


def test_metadata_basic_attr(md1612):
    assert md1612.path == '/desctabapi.aspx?c=1612'
    assert md1612.url == 'http://api.sidra.ibge.gov.br/desctabapi.aspx?c=1612'


def test_metadata_raw(md1612):
    assert not hasattr(md1612, '_raw')
    raw = md1612.raw
    assert hasattr(md1612, '_raw')
    raw2 = md1612.raw
    assert raw2 is raw
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, '../expected_raw_1612.txt')) as f:
        expected = f.read()
    assert raw == expected


def test_parse(md1612):
    md1612.parse()
    new_attrs = ['active', 'title', 'research', 'dates', 'last_date', 'vars',
                 'options', 'territory']
    for attr in new_attrs:
        assert hasattr(md1612, attr)

    assert md1612.active == True
    assert md1612.title == 'Area plantada, area colhida, quantidade produzida, rendimento medio e valor da producao das lavouras temporarias'
    assert md1612.research == 'Producao Agricola Municipal'

    assert len(md1612.dates) == 45
    assert md1612.dates[:3] == ['1974', '1975', '1976']
    assert md1612.dates[-3:] == ['2016', '2017', '2018']
    assert md1612.last_date == '2018'

    assert len(md1612.vars) == 8
    var1 = {
        'code': 109,
        'name': 'Area plantada',
        'desc': 'Area plantada (Hectares) [1988 a 2018]',
        'decimals': 'casas decimais: padrao = 0, maximo = 0'
    }
    assert md1612.vars[0] == var1
    var2 = {
        'code': 1000215,
        'name': 'Valor da producao',
        'desc': 'Valor da producao - percentual do total geral (%)',
        'decimals': 'casas decimais: padrao = 2, maximo = 5',
    }
    assert md1612.vars[-1] == var2

    assert len(md1612.options) == 1
    opt0 = md1612.options[0]
    assert list(opt0.keys()) == ['code', 'name', 'count', 'values']
    assert opt0['code'] == 'C81'
    assert opt0['name'] == 'Produto das lavouras temporarias'
    assert opt0['count'] == 34

    assert len(opt0['values']) == 34
    assert opt0['values'][0] == {'code': 0, 'name': 'Total'}
    assert opt0['values'][-1] == {
        'code': 109180,
        'name': 'Triticale (em grao) [2005 a 2018]'
    }

    assert len(md1612.territory) == 6
    terr = {
        'N1': 'Brasil(1)',
        'N2': 'Grande Regiao(5)',
        'N3': 'Unidade da Federacao(27)',
        'N8': 'Mesorregiao Geografica [1990 a 2018](137)',
        'N9': 'Microrregiao Geografica [1990 a 2018](558)',
        'N6': 'Municipio(5.563)',
    }
    assert md1612.territory == terr


def test_accent_remove():
    assert 'a' == sidrapy.table._accent_remover('á')
    assert 'a' == sidrapy.table._accent_remover('à')
    assert 'a' == sidrapy.table._accent_remover('ã')
    assert 'A' == sidrapy.table._accent_remover('Á')
    assert 'A' == sidrapy.table._accent_remover('Ã')
    assert 'a' == sidrapy.table._accent_remover('a')
    assert 'A' == sidrapy.table._accent_remover('A')
    assert 'c' == sidrapy.table._accent_remover('ç')
    assert 'mes' == sidrapy.table._accent_remover('mês')
    assert 'o sapo nao lava o pe' == sidrapy.table._accent_remover(
        'o sapo não lava o pé'
    )
    assert '123' == sidrapy.table._accent_remover('123')
    assert '  ##$$%%  ' == sidrapy.table._accent_remover('  ##$$%%  ')
    for i in range(100):
        s = str(uuid.uuid4())
        assert s == sidrapy.table._accent_remover(s)


def test_parse_var():
    s = '109 Área plantada (Hectares) [1988 a 2018] - casas decimais: padrão = 0, máximo = 0'
    exp = {
        'code': 109,
        'name': 'Área plantada',
        'desc': 'Área plantada (Hectares) [1988 a 2018]',
        'decimals': 'casas decimais: padrão = 0, máximo = 0'
    }
    assert sidrapy.table._parse_var(s) == exp

    s = '1000109 Área plantada - percentual do total geral (%) [1988 a 2018] - casas decimais: padrão = 2, máximo = 5'
    exp = {
        'code': 1000109,
        'name': 'Área plantada',
        'desc': 'Área plantada - percentual do total geral (%) [1988 a 2018]',
        'decimals': 'casas decimais: padrão = 2, máximo = 5',
    }
    assert sidrapy.table._parse_var(s) == exp


def test_parse_option():
    s = '/C81/ Produto das lavouras temporárias(34):'
    exp = {
        'code': 'C81',
        'name': 'Produto das lavouras temporárias',
        'count': 34,
        'values': [],
    }
    assert exp == sidrapy.table._parse_option(s)
