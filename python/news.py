from authority import API_KEY
from json import loads
from logging import info, error
from requests import get
from sys import argv

HEADERS = {
    'Accept': 'application/json',
    'x-api-key': API_KEY
}


class NewsService:
    COMPANY_RELATION_URL = "https://openapi.companybooknetworking.com/1.0/news/company-relation"

    @classmethod
    def format_response(cls, raw_result, relation):
        parsed_result = loads(raw_result)
        relations = parsed_result['company_relation_names'][relation]
        i = 0
        response = ''

        for doc in sorted(relations.values(), key=lambda v: v['count'], reverse=True)[0:10]:
            i += 1
            response += '{}. {} [{}]\n'.format(
                i,
                doc['name'],
                'https://www.companybooknetworking.com/{}'.format(doc['ckey']))
        return response

    @classmethod
    def find_companies(cls, company_id, relation):
        url = "{}/{}".format(cls.COMPANY_RELATION_URL, company_id)
        parameters = {
            'company_relations': relation
        }
        response = get(url, headers=HEADERS, params=parameters)
        status_code = response.status_code
        if status_code != 200:
            error('Request to {} status code {}: {}'.format(url, status_code, response.text))
            return "Error handling request!"
        return cls.format_response(response.text, relation)


if __name__ == "__main__":
    query_type = argv[1]
    if query_type == 'relation':
        company_id = argv[2]
        relation_type = argv[3]
        print(NewsService.find_companies(company_id, relation_type))
    else:
        info('Unknown query type {}. I only know relation'.format(query_type))
