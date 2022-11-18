import asyncio
import validators
import requests
from typing import Union

DICT_QUERY = {
    'GET': requests.get,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'HEAD': requests.options,
    'PATCH': requests.patch,
    'CONNECT': requests.options
}
# по оптимизации можно было бы сделать запросы через коннект
# и полученные allow method парсить и запрашивать снова
# Непонятно, что выгоднее по времени будет две асихронные функции запущенные последовательно либо одна, но со всеми
# методами запросов.


async def choice_query(url: str, method: str) -> Union[dict, object]:
    '''
    Функция создают запрос с урлу с определнным методом.
    В случае неудачи, возврачает
    '''
    try:
        response = DICT_QUERY.get(method)(url=url)
    except Exception:
        return {url: 'Строка не является ссылкой'}
    return response


def get_list_url() -> list:
    '''Формирует список из полученных строк.'''
    list_strings = input('Введите произвольное количество строк через запятую: ')
    list_urls = [item.strip() for item in list_strings.split(',')]
    return list_urls


def first_check_correct(list_input_url: list) -> tuple:
    '''Проверяет на валидацию список из URL'''
    correct_url = []
    not_urls = []
    for url in list_input_url:
        if validators.url(url):
            correct_url.append(url)
            continue
        not_urls.append(url)
    return correct_url, not_urls


async def main(urls: list, response: dict) -> dict:
    '''
    Обрабатывает и отправляет запросы к поступившим URL.
    Если URL не действителен возвращает данную информацию.
    '''
    tasks = []
    for url in urls:
        if url[-1] != '/':
            url = url + '/'
        response[url] = {}
        for method in DICT_QUERY.keys():
            tasks.append(choice_query(url, method))
    results = await asyncio.gather(*tasks)
    for result in results:
        if isinstance(result, dict):
            response.update(result)
            continue
        if result.status_code != 405:
            response[result.url][result.request.method] = result.status_code
    return response


if __name__ == '__main__':
    list_urls = get_list_url()
    # Если поступают урлы без указания протокола, то строку ниже можно убрать
    # и в функцию main передать все урлы.
    write_url, not_url = first_check_correct(list_urls)
    response = {url: 'Строка не является ссылкой' for url in not_url}
    print(asyncio.run(main(write_url, response)))
