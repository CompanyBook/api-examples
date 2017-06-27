from authority import API_KEY
from companybook import API_ENDPOINT_BASE
from json import dumps, loads
from logging import info, error
from requests import get
from sys import argv

HEADERS = {
    'Accept': 'application/json',
    'x-api-key': API_KEY
}


class SearchService:
    MATCH = "{}/{}".format(API_ENDPOINT_BASE, 'search/match')
    SEARCH = "{}/{}".format(API_ENDPOINT_BASE, 'search/search')
    PARAMETERS = {
        'page': 1,
        'per_page': 10,
        'search_type': 'default'
    }

    @classmethod
    def format_response(cls, raw_result):
        parsed_result = loads(raw_result)
        result = parsed_result['result']
        docs = result['docs']
        i = 0
        response = ''
        for doc in docs:
            i += 1
            response += '{}. {} [{}]\n'.format(
                i,
                doc['name'],
                'https://www.companybooknetworking.com/{}'.format(doc['company_id']))
        return response

    @classmethod
    def search(cls, query, country='', industry=''):
        parameters = dict(cls.PARAMETERS)
        if query:
            parameters['q'] = query
        if country:
            parameters['country'] = country
        if industry != '':
            parameters['naics_6'] = industry
        url = cls.SEARCH
        response = get(url, headers=HEADERS, params=parameters)
        status_code = response.status_code
        if status_code != 200:
            error('Request to {} status code {}: {}'.format(SearchService.SEARCH, status_code, response.text))
            return "Error handling request!"
        return cls.format_response(response.text)

    @classmethod
    def company_match(cls, query):
        parameters = {
            'per_page': 5,
        }
        if query:
            parameters['q'] = query
        url = cls.MATCH
        response = get(url, headers=HEADERS, params=parameters)
        status_code = response.status_code
        if status_code != 200:
            error('Request to {} status code {}: {}'.format(SearchService.SEARCH, status_code, response.text))
            return "Error handling request!"
        return cls.format_response(response.text)


class IndustryService:
    SEARCH = "https://openapi.companybooknetworking.com/1.0/industries/industry-suggest"
    PARAMETERS = {
        'page': 1,
        'per_page': 10,
        'search_type': 'default'
    }
    MAX_NUMBER = 9

    @classmethod
    def parse_query(cls, command):
        return command.lstrip().rstrip()

    @classmethod
    def search(cls, query, country):
        parsed_query = cls.parse_query(query)
        parameters = dict(cls.PARAMETERS)
        parameters.update({'q': parsed_query})
        if country != '':
            parameters.update({'search_country_iso': country})
        url = cls.SEARCH
        response = get(url, headers=HEADERS, params=parameters)
        return cls.format_response(response.text)

    @classmethod
    def format_response(cls, raw_result):
        parsed_result = loads(raw_result)
        result = parsed_result['industries']
        summary = result['summary']
        i = 1
        top = summary['top']
        response = '{}. {} [{}]\n'.format(i, top['title'], top['code'])
        for doc in summary['related'][:cls.MAX_NUMBER]:
            i += 1
            response += '{}. {} [{}]\n'.format(i, doc['title'], doc['code'])
        return response


if __name__ == "__main__":
    search_type = argv[1]
    query = argv[2]
    country = industry = ''
    if len(argv) > 3:
        country = argv[3].upper()
    if len(argv) > 4:
        industry = argv[4]
    if search_type == 'search':
        print(SearchService.search(query, country, industry))
    elif search_type == 'industry':
        print(IndustryService.search(query, country))
    elif search_type == 'match':
        print(SearchService.company_match(query))
    else:
        info('Unknown search type {}. I only know search, industry and match (find company)'.format(search_type))
