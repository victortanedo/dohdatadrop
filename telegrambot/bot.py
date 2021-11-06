import requests
from bottle import (run, post, response, request as bottle_request)

BOT_URL = 'https://api.telegram.org/bot2103396271:AAF-pgJgQxKzn4UtJHLsDWvxZX1j1d4q6XQ/'

def get_chat_id(data):
    '''Method to extract chat id from telegram request '''
    chat_id = data['message']['chat']['id']
    return chat_id

def get_message(data):
    '''Method to extract message id from telegram request '''
    message_text = data['message']['text']
    return message_text

def send_message(prepared_data):
    '''Prepared data should be json which includes at least `chat_id` and `text` '''
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)

def parse_message_data(text):
    if text.startswith('case_search: '):
        tokens = text.split(' ')
        url = r'http://127.0.0.1:8000/case/' + tokens[1]
        r = requests.get(url)

        data = r.json()

        text = f"Case Code: {data['case_code']}\n\
Age: {data['age']}\n\
Age Group: {data['age_group']}\n\
Sex: {data['sex']}\n\
Date Specimen: {data['date_specimen']}\n\
Date Result Release: {data['date_result_release']}\n\
Date Rep Conf: {data['date_rep_conf']}\n\
Date Died: {data['date_died']}\n\
Date Recovered: {data['date_recovered']}\n\
Removal Type: {data['removal_type']}\n\
Admitted: {data['admitted']}\n\
Region Res: {data['region_res']}\n\
Prov Res: {data['prov_res']}\n\
City Mun Res: {data['city_mun_res']}\n\
City Muni PSGC: {data['city_muni_psgc']}\n\
Baragay Res: {data['barangay_res']}\n\
Barangay PSGC: {data['barangay_psgc']}\n\
Health Status: {data['health_status']}\n\
Quarantined: {data['quarantined']}\n\
Date Onset: {data['date_onset']}\n\
Pregnant: {data['pregnant']}\n\
Validation Status: {data['validation_status']}\n\
"
            
    elif text.startswith('total '):
        tokens = text.split(' ')
        dates = tokens[1].split('/')

        url = r'http://127.0.0.1:8000/total/' + dates[2] + '/' + dates[0] + '/' + dates[1] + '/' + tokens[2]

        r = requests.get(url)

        data = r.json()

        text = f"Date: {data['date']}\n\
Age: {data['age']}\n\
Recovered Count: {data['recovered_count']}\n\
Died Count: {data['died_count']}\n\
On-Going: {data['on_going']}"        

    elif text.startswith('list '):
        tokens = text.split(' ')
        dates = tokens[1].split('/')

        url = r'http://127.0.0.1:8000/list/' + dates[2] + '/' + dates[0] + '/' + dates[1] + '/' + tokens[2]

        r = requests.get(url)

        data = r.json()

        text = ''
        for d in data:
            text += f"Date: {d['date']}\n\
Status: {d['status']}\n\
Case Code: {d['case_number']}\n\
Gender: {d['gender']}\n\
Date Reported: {d['date_reported']}\
\n\n"
    else:
        text = 'Invalid Command'

    print(text)
    return text

def prepare_data_for_answer(data):
    answer = parse_message_data(get_message(data))
    json_data = {
        'chat_id': get_chat_id(data),
        'text': answer,
    }

    return json_data

@post('/') # out python function based endpoint
def main():
    data = bottle_request.json # extract all request data
    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)

    return response

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)

