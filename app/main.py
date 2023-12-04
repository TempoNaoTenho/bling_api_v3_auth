import os

from modules import bling
from usage_example import bling_api_call_example, get_tokens_with_code_example

def main():
    """Code example. Needs the url redirection code
    (currenlty being retrieved with input for example purposes).

    Info on image about how to get the code url param"""

    token_handler = bling.BlingApiTokenHandler()
    token_storage = bling.TokenStorage()

    # First time runing since the credential folder doesn't exist
    # yet and json is setted as the default storage
    credentials_folder = os.path.join(os.getcwd(), 'credential')
    first_time_runing = not os.path.exists(credentials_folder)

    if first_time_runing:
        code = input('Url redirection code: ')  # Manually retrieved or your fancy code
        get_tokens_with_code_example(code, token_handler)

    api_call = bling_api_call_example(token_storage, token_handler)
    print(api_call)

if __name__ == '__main__':
    main()
