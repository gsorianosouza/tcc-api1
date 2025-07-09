# TCC API

 Este repositório contém a API desenvolvida com FastAPI para o nosso TCC. Ela será responsável por gerenciar e fornecer os dados utilizados no sistema que estamos construindo.

## Como rodar o projeto

#### Clone o repositório

```bash
  git clone https://github.com/GuhLoyola/tcc-api.git
  cd tcc-api
```

#### Crie e ative o ambiente virtual

*Windows*

```bash
    python -m venv .venv
    .venv\Scripts\activate
```

*Linux*

```bash
    python -m venv .venv
    source .venv/bin/activate
```

Caso estiver utilizando *Git Bash*, substitua o **bin** por **Scripts** no comando acima.

#### Instale as dependências

```bash
    pip install -r requirements.txt
```

#### Crie as tabelas no banco de dados

Antes de iniciar o servidor, execute o comando abaixo para criar as tabelas no banco de dados:

```bash
    python -m db.init_db
```

Por enquanto é necessário ter o banco criado no editor (PgAdmin, DBeaver, etc).

#### Treine o modelo de Machine Learning

Antes de iniciar a aplicação é necessário treinar o modelo de ML, para isso execute o código abaixo:

```bash
   python model/training/train_model.py
```

#### Rode a aplicação local

```bash
    uvicorn main:app --reload
```

### Tecnologias 🧰

- Python 3.11+

- FastAPI

- Uvicorn

### Status do projeto 🚧

Em desenvolvimento
