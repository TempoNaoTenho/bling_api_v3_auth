from modules.bling import BlingApiTokenHandler, TokenStorage


def get_tokens_with_code_example(code,
                                 token_handler: BlingApiTokenHandler):
    """
    - Retrieve the access token using the code param.
      This code is used to get the access and refresh tokens.
      It has to be manually copied from the URL generated on Bling App Config.

    - Obtem o token de acesso usando o código.
      Este código é usado para obter os tokens de acesso e de atualização.
      Ele deve ser copiado manualmente da URL gerada no App Bling.

    Args:
        code: str
        token_handler: BlingApiTokenHandler

    Returns:
        None
    """

    return token_handler.get_token_using_code(code)


def refresh_tokens_example(refresh_token: str,
                           token_handler: BlingApiTokenHandler):
    """
    - Gets the access and refresh tokens using the code returned by
      the get_tokens_with_code() method.
    - Atualiza o access_token e o refresh_token
      usando o token de atualização armazenado.

    Args:
        token_storage: TokenStorage
        token_handler: BlingApiTokenHandler

    Returns:
        None
    """

    return token_handler.refresh_tokens(refresh_token)

def get_valid_access_token(token_storage: TokenStorage,
                           token_handler: BlingApiTokenHandler):
    """
    Return a valid access token, refreshing it only when needed.
    """
    access_token = token_storage.retrieve_token_by_key('access_token')
    if access_token and not token_storage.is_token_expired('access_token'):
        return access_token

    refresh_token = token_storage.retrieve_token_by_key('refresh_token')
    if not refresh_token:
        return None

    token_handler.refresh_tokens(refresh_token)
    return token_storage.retrieve_token_by_key('access_token')

def bling_api_call_example(token_storage: TokenStorage,
                  token_handler: BlingApiTokenHandler) -> str:

    """
    - Simulate a complete API call using the access and refresh tokens.
    - Simule uma chamada completa de API usando os tokens de acesso e de atualização.

    Args:
        token_storage: TokenStorage
        token_handler: BlingApiTokenHandler

    Returns:
        str
    """

    access_token = get_valid_access_token(token_storage, token_handler)
    refresh_token = token_storage.retrieve_token_by_key('refresh_token')

    print('access_token: ', access_token)
    print('refresh_token: ', refresh_token)

    if access_token:
        # YOUR API CALLS HERE
        """
            headers = {'Authorization': f'Bearer {access_token}'}
            request = requests.Session()
            resp = request.get(url, headers=headers)
            ...
            ...
            data = resp.json()
            return data"""

        return 'Example success!'
