# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'


def log_errors(func0):
    def decor(param):
        try:
            func0(param)
        except Exception as excs:
            with open('function_errors.txt', 'a') as file:
                s = f'<{func0.__name__}> <{str(param)}> <{excs.__class__.__name__}> <{excs}>'
                file.write(s)
                file.write('\n')
            #  Зря закомментировали raise. По условиям задания после логирования,
            #  исключение нужно выбросить снова.
            raise

    return decor


# Проверить работу на следующих функциях
@log_errors
def perky(param):
    return param / 0


@log_errors
def check_line(sline):
    name, email, age = sline.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')
perky(param=42)


# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла

# Попробуйте сделать усложнённую версию задания.
def log_errors1(file_name):
    def _log_errors(func_adv1):
        def decor():
            try:
                return func_adv1()
            except Exception as excs:
                with open(file_name, 'a') as file:
                    s = f'<{func_adv1.__name__}> <{excs.__class__.__name__}> <{excs}>'
                    file.write(s)
                    file.write('\n')
                #  Зря закомментировали raise. По условиям задания после логирования,
                #  исключение нужно выбросить снова.
                raise

        return decor

    return _log_errors


@log_errors1(file_name='function_errors.log')
def func_adv():
    return 1 / 0


a = func_adv()
print(str(a))

# Зачёт!
