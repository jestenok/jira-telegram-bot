
kek = {}



print(kek)


def handler(text):
    def dec(func):
        kek[text] = func

        def wrapper(*args):
            func(*args)
        return wrapper
    return dec


@handler('/start')
def f1(text):
    print('Я отработал нахой' + text)


@handler('default')
def qweqwe(text):
    print('qweqwedavsgshnedjrtmy')


text = '/start'

kek['/start']('qwerqwer')


f1('qwerqwersggdrzgdrgrg')