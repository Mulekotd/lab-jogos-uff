# Lab Jogos UFF

Repositório voltado para a disciplina de Laboratório de Programação de Jogos. 

## Setup

```py
python -m venv .env
./.env/Scripts/activate # windows
source .env/bin/activate # linux or macOS
pip install pygame
```

## Run project

Para rodar qualquer projeto é necessário adicionar o diretório external à variável de ambiente PYTHONPATH.

```sh
# Exemplo: para rodar o projeto space_invaders
$env:PYTHONPATH="external"; python space_invaders/main.py # windows
PYTHONPATH=external python space_invaders/main.py # linux or macOS
```
