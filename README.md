# TCC API

Este repositório contém a API desenvolvida com FastAPI para o nosso TCC. Ela será responsável por gerenciar e fornecer os dados utilizados no sistema que estamos construindo.

## Como rodar

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

#### Rode a aplicação local

```bash
    uvicorn main:app --reload
```

### Tecnologias 🧰

- Python 3.11+

- FastAPI

- Uvicorn

- SQLAlchemy / ORM

### Status do projeto 🚧

Em desenvolvimento
