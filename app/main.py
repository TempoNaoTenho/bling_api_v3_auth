from modules import bling
from usage_example import bling_api_call_example, get_tokens_with_code_example

def main():
    """Code example. Needs the url redirection code
    (currently being retrieved with input for example purposes).

    Info on image about how to get the code url param"""

    token_handler = bling.BlingApiTokenHandler()
    token_storage = bling.TokenStorage()

    refresh_token = token_storage.retrieve_token_by_key('refresh_token')
    if not refresh_token:
        code = input('Url redirection code: ')  # Manually retrieved or your fancy code
        get_tokens_with_code_example(code, token_handler)

    api_call = bling_api_call_example(token_storage, token_handler)
    print(api_call)

if __name__ == '__main__':
    main()
