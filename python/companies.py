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


class CompaniesService:
    COMPANY_INFORMATION_URL = "{}/{}".format(API_ENDPOINT_BASE, 'companies/company')

    @classmethod
    def format_response(cls, raw_result):
        parsed_result = loads(raw_result)
        company = parsed_result['company']
        fields = company['fields']
        name = fields['name']['sources']['MERGED']
        category = fields['naics']['sources']['MERGED']['primary']
        location_type = fields['location_type']['sources']['HOOVERS']
        revenue = fields['finance_latest']['sources']['MERGED']['total_revenues']
        response = {
            'name': name,
            'location_type': location_type,
            'category': category,
            'revenue': revenue
        }
        return dumps(response)

    @classmethod
    def find_information(cls, company_id):
        url = "{}/{}".format(cls.COMPANY_INFORMATION_URL, company_id)
        response = get(url, headers=HEADERS)
        status_code = response.status_code
        if status_code != 200:
            error('Request to {} status code {}: {}'.format(url, status_code, response.text))
            return "Error handling request!"
        return cls.format_response(response.text)


if __name__ == "__main__":
    query_type = argv[1]
    if query_type == 'info':
        company_id = argv[2]
        print(CompaniesService.find_information(company_id))
    else:
        info('Unknown query type {}. I only know info'.format(query_type))
