from authority import API_KEY
from json import dumps, loads
from logging import error
from requests import get


class SearchService:
    SEARCH = 'https://openapi.companybooknetworking.com/1.0/search/search?'


HEADERS = {
    'Accept': 'application/json',
    'x-api-key': API_KEY
}


def format_result(result):
    return {
        'url': 'https://www.companybooknetworking.com/{}'.format(result['company_id']),
        'name': result['name'],
        'snippet': result['query_snippet'] if 'query_snippet' in result else ''
    }


def format_response(raw_result):
    parsed_result = loads(raw_result)
    result = parsed_result['result']
    docs = result['docs']
    resultset = [format_result(doc) for doc in docs]
    return resultset


def search(query, country=''):
    parameters = {}
    if query:
        parameters['q'] = query
    if country:
        parameters['country'] = country
    response = get(SearchService.SEARCH, headers=HEADERS, params=parameters)
    status_code = response.status_code
    if status_code != 200:
        error('Request to {} status code {}: {}'.format(SearchService.SEARCH, status_code, response.text))
        return "Error handling request!"
    return (dumps(format_response(response.text)))
