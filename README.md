# - Português

## Descrição

Exemplo simples de código para autenticação OAuth2 com a `API do Bling (V3)` utilizando Python.
Por padrão o projeto funciona sem Redis, usando armazenamento em JSON local.

Pode ser configurado para armazenar os dados em formato JSON ou utilizando o Redis, definindo `TOKENS_STORAGE_METHOD=json|redis` no `.env`. O padrão é `json` (sem Redis).

Um exemplo de uso está no arquivo `app/usage_example.py`.

-------------------------------------

Importante: o refresh token tem uma validade de 30 dias, conforme documentação da API [https://developer.bling.com.br/aplicativos#refresh-token](https://developer.bling.com.br/aplicativos#refresh-token), 

-------------------------------------


## Instalação

```bash
git clone https://github.com/TempoNaoTenho/bling_api_v3_auth.git
python -m venv venv
Linux (source venv/bin/activate) ou Windows(venv/Scripts/activate)
pip install -r requirements.txt
```

Para habilitar Redis, instale as dependências opcionais:

```bash
pip install -r requirements-redis.txt
```
## Configuração inicial

- Crie um arquivo `.env` na raiz do projeto (você pode copiar de `.env.example`):

```bash
BLING_CLIENT_ID=SEU_CLIENT_ID
BLING_CLIENT_SECRET=SEU_CLIENT_SECRET
```

Para uso com Redis, as variáveis do `.env` são REDIS_HOST_IP, REDIS_HOST_PORT, REDIS_PASSWORD


## Obter os tokens:

- O `client_id` e `client_secret` são obtidos ao cadastrar aplicativo na sua conta do Bling. Veja o link [https://developer.bling.com.br/aplicativos](https://developer.bling.com.br/aplicativos)


- O `code` necessário para a primeira execução do script é obtido através do endereço "Link do convite" da sua conta do Bling
![image](code-link-bling.jpg)

- Com o `code` você tem 1 minuto para obter o `refresh token`. (Neste ponto é só rodar o script e colar o code ou passar o parâmetro para a função `get_tokens_with_code_example(code)`).

## Executar o script

```bash
python app/main.py
```

Os tokens são armazenados em `credential/credentials.json` (ignorado pelo git).

# - English

## Description

Example code to authenticate with the `Bling (V3) API` using OAuth2 in Python.

It can be configured to store the data in JSON format or using Redis by setting `TOKENS_STORAGE_METHOD=json|redis` in the `.env` file. The default is `json`.

An example of usage is in the file `app/usage_example.py`.

-------------------------------------

Important: the refresh token has a validity of 30 days according to the Bling API [https://developer.bling.com.br/aplicativos#refresh-token](https://developer.bling.com.br/aplicativos#refresh-token),

-------------------------------------


## Install

```bash
git clone https://github.com/TempoNaoTenho/bling_api_v3_auth.git
python -m venv venv
Linux (source venv/bin/activate) or Windows(venv/Scripts/activate)
pip install -r requirements.txt
```

## Configuration

- Create an `.env` file at the project root (you can copy from `.env.example`):

```bash
BLING_CLIENT_ID=YOUR_CLIENT_ID
BLING_CLIENT_SECRET=YOUR_CLIENT_SECRET
```

For use with redis, the variables in the `.env` file are REDIS_HOST_IP, REDIS_HOST_PORT, REDIS_PASSWORD.

To enable Redis support, install the optional dependencies:

```bash
pip install -r requirements-redis.txt
```


## Get tokens:

- The `client_id` and `client_secret` are obtained when registering your app on Bling. See the link [https://developer.bling.com.br/aplicativos](https://developer.bling.com.br/aplicativos)


- The `code` is required to get the `refresh token`. (At this point, you can run the script and paste the code or pass the parameter to the function `get_tokens_with_code_example(code)`).

## Run the script

```bash
python app/main.py
```

Tokens are stored at `credential/credentials.json` (git-ignored).
