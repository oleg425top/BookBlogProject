from django import template

register = template.Library()


@register.filter(name='pluralize_ru')
def pluralize_ru(value, arg='результат,результата,результатов'):
    """
    Кастомный фильтр для склонения слов на русском языке.
    Пример использования: {{ total_results|pluralize_ru:'результат,результата,результатов' }}
    """
    args = arg.split(',')
    number = int(value)

    if len(args) != 3:
        return ''

    if number % 10 == 1 and number % 100 != 11:
        return args[0]
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return args[1]
    else:
        return args[2]
