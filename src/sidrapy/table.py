import re
import logging
from enum import Enum

import pandas as pd
from lxml.html.soupparser import fromstring

import sidrapy.server


logger = logging.getLogger()


class Table:
    def __init__(self, code: int):
        if not isinstance(code, int):
            msg = f'Code must be "int". But "{type(code)}" given'
            raise TypeError(msg)
        if code <= 0:
            msg = f'Code value must be greater then 0. But "{code}" was given'
            raise ValueError(msg)
        self.code = code

    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            self._metadata = Metadata(self)
        return self._metadata

    def __str__(self):
        return f'<Table: {self.code}>'


class Metadata:
    def __init__(self, table: Table):
        self.table = table

    @property
    def path(self):
        return '/desctabapi.aspx?c=' + str(self.table.code)

    @property
    def url(self):
        return sidrapy.server.create_url(self.path)

    @property
    def raw(self):
        if not hasattr(self, '_raw'):
            resp = sidrapy.server.get(self.path)
            tree = fromstring(resp)
            text = tree.xpath('//text()')
            text = ''.join(text)
            text = re.sub('<!--(.|\n)+-->', '', text)
            text = re.sub(r'^([\s\S]+)\/T\/', r'/T/', text)
            text = re.sub('\r', '\n', text)
            text = re.sub('\xa0', ' ', text)
            text = re.sub('\t', ' ', text)
            text = re.sub('\n{2,}', '\n', text)
            text = re.sub(r'\s{2,}', ' ', text)
            self._raw = text
        return self._raw

    def parse(self):
        """
        This method parses the raw description text

        It works like a state machine to get following info:
        active -> bool
        title -> str
        research -> str
        subject -> str
        dates -> [str]
        last_date -> str
        vars -> a list of dict
            each dict has a code (int), a name (str) and decimals (str) info
        options -> a list of dict
            each dict has a code (str), a name (str), a count(int) and values
            value is a list of dict.
                each dict has a code (int) and a name (str)
        territory -> as list of dict
            each dict has a code (str) and a name(str)
        """

        text = self.raw
        text = _accent_remover(text)
        lines = text.split('\n')

        state = '0'
        for n in range(len(lines)):
            line = lines[n]

            if line.startswith('/T/ '):
                state = 'header'
                line = line.split()
                assert line[2] == str(self.table.code)
                self.title = ' '.join(line[4:])

            elif state == 'header' and line.startswith('Pesquisa'):
                self.research = line[10:]

            elif state == 'header' and line.startswith('Assunto'):
                self.subject = line[9:]

            elif state == 'header' and line.startswith('/P/'):
                self.dates = line[line.find(':') + 2:].split(', ')
                self.last_date = self.dates[-1]

            elif state == 'header' and line.startswith('/V/'):
                state = 'vdims'
                vdims = re.findall(r'\((\d+)\)', line)
                assert len(vdims) == 1
                vdims = int(vdims[0])

            elif state == 'vdims' and not line.startswith('/'):
                var = _parse_var(line)
                if not hasattr(self, 'vars'):
                    self.vars = []
                self.vars.append(var)

            elif state in {'vdims', 'options'} and line.startswith('/'):
                state = 'options'
                option = _parse_option(line)
                if not hasattr(self, 'options'):
                    self.options = []
                self.options.append(option)

            elif state == 'options' and not line.startswith('Niveis'):
                if line[0].isdigit():
                    d = {
                        'code': int(line.split(' ')[0]),
                        'name': ' '.join(line.split(' ')[1:]),
                    }
                    self.options[-1]['values'].append(d)
                elif line[0] == '[':
                    # date range
                    self.options[-1]['values'][-1]['name'] += ' ' + line
                else:
                    # noise
                    pass

            elif state == 'options' and line.startswith('Niveis'):
                state = 'territory'
                self.territory = {}

            elif state == 'territory' and not line.startswith('Nota:'):
                if line.startswith('/'):
                    code = line.replace('/', '')
                    name = lines[n + 1]
                    name = name.replace(' Listar unidades territoriais', '')
                    self.territory[code] = name

            elif state == 'territory' and line.startswith('Nota:'):
                break

            else:
                msg = f'State machine error. {state=}; {line=}'
                raise RuntimeError(msg)

        assert len(self.vars) == vdims

        self.active = '(serie encerrada)' not in self.title


def _parse_option(line: str) -> dict:
    "Parses a option header line from raw description"

    d = {}
    try:
        d['code'] = re.search(r'/(.+)/', line).groups()[0]
    except AttributeError:
        logger.error(f'{line=}')
        raise
    d['name'] = re.search(r'\s(.+)\(', line).groups()[0]
    d['count'] = int(re.search(r'\((\d+)\):', line).groups()[0])
    d['values'] = []
    return d


def _parse_var(line: str) -> dict:
    "Parses a variable line from raw description"

    d = {}
    d['code'] = int(re.search(r'^\d+', line).group())
    d['name'] = re.search(r'^\d+\s(.+?)(\s-\s|\s\()', line).groups()[0]
    d['desc'] = re.search(r'^\d+\s(.+?) - casas decimais', line).groups()[0]
    d['decimals'] = re.search(r'casas decimais.+', line).group()
    return d


def _accent_remover(text: str) -> str:
    "Removes special portuguese chars form a string"

    d = {
        'a': 'áàãâ',
        'e': 'éê',
        'i': 'íï',
        'o': 'óõôö',
        'u': 'ú',
        'c': 'ç',
    }
    for k, v in d.items():
        text = re.sub(f'[{v}]', k, text)
        text = re.sub(f'[{v.upper()}]', k.upper(), text)
    return text
