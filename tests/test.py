from testld.check_string import get_list_url


def test_list_url():
    assert isinstance(get_list_url(), list), 'Функция возвращает не список'
