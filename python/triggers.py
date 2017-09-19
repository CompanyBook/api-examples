from authority import API_KEY
from companybook import API_ENDPOINT_BASE
from json import loads
from logging import info, error
from requests import get
from sys import argv

HEADERS = {
    'Accept': 'application/json',
    'x-api-key': API_KEY
}

PARAMETERS = {
    'confidence_level': 'relaxed',
    'per_page': 10,
    'search_id': 3,
    'show_data_for': 'articles'
}

class TriggerService:
    COMPANY_TRIGGER_URL = "{}/{}".format(API_ENDPOINT_BASE, 'news/news-triggers/')
    TOPIC_TRIGGER_URL = "{}/{}".format(API_ENDPOINT_BASE, 'news/news-triggers-search')

    @classmethod
    def format_response(cls, raw_result):
        parsed_result = loads(raw_result)
        articles = parsed_result['articles']
        response = ''
        for i, article in enumerate(articles):
            sentences_companies = [sentence['companies'] for sentence in article['sentences']]
            all_companies = []
            for companies in sentences_companies:
                if 'strict' in companies:
                    [all_companies.append(company) for company in companies['strict']]
            companies = set(all_companies)
            response += "{}. {} [{}] - {}\n".format(
                i + 1,
                article['title'],
                article['url'],
                ', '.join(companies)
            )
        return response

    @classmethod
    def find_company_triggers(cls, company_id, trigger):
        url = cls.COMPANY_TRIGGER_URL + company_id
        parameters = dict(PARAMETERS)
        parameters['triggers'] = trigger
        return cls.retrieve(url, parameters)

    @classmethod
    def retrieve(cls, url, parameters):
        response = get(url, headers=HEADERS, params=parameters)
        status_code = response.status_code
        if status_code != 200:
            error("Request to {} status code {}: {}".format(url, status_code, response.text))
            return "Error handling request"
        return cls.format_response(response.text)

    @classmethod
    def find_topic_triggers(cls,  topic, trigger):
        parameters = dict(PARAMETERS)
        parameters['topic_query'] = topic
        parameters['triggers'] = trigger
        url = cls.TOPIC_TRIGGER_URL
        return cls.retrieve(url, parameters)


if __name__ == "__main__":
    trigger_type = argv[1]
    trigger = argv[2]
    if trigger_type == 'company':
        company_id = argv[3]
        print(TriggerService.find_company_triggers(company_id, trigger))
    elif trigger_type == 'topic':
        topic = '+'.join(argv[3:]).replace(' ', '+')
        print(TriggerService.find_topic_triggers(topic, trigger))
    else:
        info("Unknown trigger type {}. I only know company and topic".format(trigger_type))