# Gringozin VIP — pacote completo

Este pacote serve o HTML e o backend no mesmo domínio. Assim, login, IP, status e switches funcionam sem o erro causado por abrir apenas um HTML estático.

## Instalação local

Linux/macOS:

```bash
chmod +x run.sh
./run.sh
```

Depois abra `http://localhost:5000`.

Windows com Python instalado:

```bat
python -m venv .venv
.venv\\Scripts\\pip install -r requirements.txt
.venv\\Scripts\\python app.py
```

## Publicar no Render

A forma mais simples é subir esta pasta para um repositório GitHub e criar um Web Service apontando para ele. O `render.yaml` já contém:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
- `FLASK_SECRET` gerado automaticamente

Defina a variável `ACCESS_KEY` no Render com a chave desejada. O padrão local é `GRINGOZIN803`.

## O que foi corrigido

- O frontend e as APIs usam a mesma origem.
- A chave não fica mais escrita no JavaScript.
- O IP é obtido no servidor e aparece após o login.
- Os switches retornam erro visível e voltam ao estado anterior se a API falhar.
- As configurações são persistidas em `gringozin.sqlite3`.

> Este projeto implementa o painel web, autenticação e registro das configurações. Os nomes das opções não executam injetor, bypass, aimbot ou alteração de jogo automaticamente. Para qualquer integração externa, use somente software autorizado e APIs documentadas.
