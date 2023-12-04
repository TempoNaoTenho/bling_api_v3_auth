from modules.bling import BlingApiTokenHandler, TokenStorage


def get_tokens_with_code_example(code, 
                                 token_handler: BlingApiTokenHandler):
        
    return token_handler.get_token_using_code(code)

    
def refresh_tokens_example(refresh_token: str,
                           token_handler: BlingApiTokenHandler):
    
    return token_handler.refresh_tokens(refresh_token)
    
    
def bling_api_call_example(token_storage: TokenStorage,
                  token_handler: BlingApiTokenHandler):
        
    refresh_tokens_example(
        token_storage.retrieve_token_by_key('refresh_token'), 
        token_handler)

    access_token = token_storage.retrieve_token_by_key('access_token')
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
    
    



