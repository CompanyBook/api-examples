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


class SimilarCompaniesService:
    COMPANY_URL = "{}/{}".format(API_ENDPOINT_BASE, 'similar-companies/company')

    @classmethod
    def format_response(cls, raw_result):
        parsed_result = loads(raw_result)
        docs = parsed_result['similar']
        i = 0
        response = ''
        for doc in docs[0:10]:
            i += 1
            response += '{}. {} [{}]\n'.format(
                i,
                doc['name'],
                'https://www.companybooknetworking.com/{}'.format(doc['key']))
        return response

    @classmethod
    def find_companies(cls, company_id):
        url = "{}/{}".format(cls.COMPANY_URL, company_id)
        response = get(url, headers=HEADERS)
        status_code = response.status_code
        if status_code != 200:
            error('Request to {} status code {}: {}'.format(url, status_code, response.text))
            return "Error handling request!"
        return cls.format_response(response.text)


if __name__ == "__main__":
    query = argv[1]
    print(SimilarCompaniesService.find_companies(query))
