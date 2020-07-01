# Como contribuir com o sidrapy
Obrigado por considerar contribuir com sidrapy!

## Suporte
Por favor, não use o issue tracker para isso.
O issue tracker é uma ferramenta para resolver bugs e solicitações de recursos no sidrapy.
Use nosso grupo no Telegram para perguntas sobre o uso do sidrapy ou dificuldades com seu próprio código:
* [Grupo Telegram](https://t.me/joinchat/AmdQix1KKeZ5KGpsKVFsKw)

## Relatando problemas
Inclua as seguintes informações em sua postagem:
* Descreva o que você esperava que acontecesse.
* Se possivel, inclua um [exemplo reprodutível mínimo](https://pt.stackoverflow.com/help/minimal-reproducible-example) para nos ajudar a identificar o problema.
Isso também ajuda a verificar se o problema não está no seu próprio código.
* Descreva o que realmente aconteceu. Inclua o rastreamento completo, se houver uma exceção.
* Liste as versões do seu python e o sidrapy.
Se possível, verifique se esse problema já foi corrigido nas versões mais recentes ou no código mais recente no repositório.

## Submetendo correções
Se não houver uma Issue em aberto para o que você deseja enviar, prefira abrir uma para discussão antes de trabalhar em uma PR.
Você pode trabalhar em qualquer Issue que não tenha uma PR aberto vinculado à ela ou a um mantenedor atribuído a ele.
Eles aparecem na barra lateral.
Não é necessário perguntar se você pode resolver um problema que lhe interessa.

Inclua o seguinte na sua correção:
* Use o [Black](https://black.readthedocs.io/) para formatar seu código. Essa e outras ferramentas executarão automaticamente se instalar o [pre-commit](https://pre-commit.com/) utilizando as instruções abaixo.
* Inclua testes se a sua correção adicionar ou alterar o código. Verifique se o teste falhou sem a sua correção.
* Atualize qualquer página ou string de documentação relevante. As páginas e strings de documentação devem ser quebradas em 72 caracteres.

### Configuração inicial
* Baixe e instale a [ultima versão do git](https://git-scm.com/downloads).

* Configure o git com seu [usuário](https://help.github.com/pt/github/using-git/setting-your-username-in-git) e [email](https://help.github.com/pt/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address).
```shell script
$ git config --global user.name 'your name'
$ git config --global user.email 'your email'
```

* Tenha certeza que possui uma [conta no GitHub](https://github.com/join).

* Faça um fork do sidrapy  para sua conta do Github clicando no botão [Fork](https://github.com/AlanTaranti/sidrapy/fork).

* [Clone](https://help.github.com/pt/github/getting-started-with-github/fork-a-repo#step-2-create-a-local-clone-of-your-fork) o repositório principal localmente.
```shell script
$ git clone https://github.com/AlanTaranti/sidrapy
$ cd sidrapy
```

* Adicione seu fork como repositorio remoto para submeter seu trabalho também. Substitua `{usuario}` como o seu usuário.
Esse define o seu repositório remoto como "fork", enquanto o repositório remoto padrao AlanTaranti é "origin".
```shell script
$ git remote add fork https://github.com/{usuario}/sidrapy
```

* Crie um virtualenv.
```shell script
$ python3 -m venv venv
$ . venv/bin/activate
```

No Windows, ativar o virtualenv é diferente.
```shell script
> env\Scripts\activate
```

* Instale o sidrapy no modo editavel com as dependencias de desenvolvimento.
```shell script
$ pip install -e . -r requirements/dev.txt
```

* Opcional: Instale os hooks pre-commit.
```shell script
$ pre-commit install
```

### Come a desenvolver

* Crie uma branch para identificar a Issue que gostaria de trabalhar.
Se você está submetendo uma correção de bug ou documentação, ramifique da última versão ".x".
```shell script
$ git fetch origin
$ git checkout -b your-branch-name origin/0.1.x
```

* Se você está submetendo uma adição ou troca recursos, ramifique da branch "develop".
```shell script
$ git fetch origin
$ git checkout -b your-branch-name origin/develop
```

* Usando seu editor favorito, faça suas alterações, [committing no percurso](https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes).

* Inclua testes que cubram todas as alterações de código que você fizer.
Verifique se o teste falhou sem a sua correção. Execute os testes conforme descrito abaixo.

* Submeta os commits do seu fork no GitHub e [crie uma pull request](https://help.github.com/pt/articles/creating-a-pull-request).
Conecte à Issue sendo tratada com `fixes #123` na pull request.
```shell script
$ git push --set-upstream fork your-branch-name
```

### Executando os testes
Execute a suite básica de testes com o pytest.
```shell script
$ pytest -v
```
Esse comando executa os testes no ambiente atual, que normalmente é suficiente.
O CI executará a suite completa de testes quando submeter a pull request.

Você pode executar o conjunto completo de testes com o tox, caso não queira esperar o CI.
```shell script
$ tox
```

### Executando a cobertura de testes
A geração de um relatório de linhas que não possuem cobertura de teste pode indicar por onde começar a contribuir.
Execute pytest usando o coverage e gere um relatório.
```shell script
$ pytest --cov=src --cov-report=term-missing
```
O report será exibito na tela
Saiba mais sobre o [pytest-cov](https://github.com/pytest-dev/pytest-cov).
