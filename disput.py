import requests
import json
import pprint

url_questions='https://dispute.kzn.ru/api/disputes/553/questions.json?page={}'
url_suggestions='https://dispute.kzn.ru/api/disputes/553/suggestions.json?page={}'

cookies = {
    '_disputekzn_session': '',
}

def getPages(url):
    response = requests.get(url.format(0), cookies=cookies)
    j = json.loads(response.text)
    count = j['meta']['total_records']
    print('Количество: {}'.format(count))
    pages_count = 1 + count // 10
    pages = {}
    for p in range(pages_count):
        response = requests.get(url.format(p+1), cookies=cookies)
        pages[p] = json.loads(response.text)
    return pages


def savePages(name, pages):
    i = 1
    for p in pages:
        page = pages[p]
        #print(question)
        with open('{}_page_{}'.format(name, i), 'w') as file:
            file.write(json.dumps(page, ensure_ascii=False))
        i += 1


print('Вопросы')
questions = getPages(url_questions)
savePages('questions', questions)

for p in questions:
    question_page = questions[p]
    data = question_page['data']
    for data_i in data:
        question_text = data_i['data_user']['data']['text']
        print('*'*50)
        print('Вопрос\n\n{}\n'.format(question_text))
        decisions = data_i['decisions']
        for decision in decisions:
            answer_text = decision['text']
            print('Ответ\n\n{}\n'.format(answer_text))


print('\nПредложения')
suggestions = getPages(url_suggestions)
savePages('suggestions', suggestions)


for p in suggestions:
    suggestion_page = suggestions[p]
    data = suggestion_page['data']
    for data_i in data:
        question_text = data_i['data_user']['data']['text']
        print('*'*50)
        print('Предложение\n\n{}\n'.format(question_text))
