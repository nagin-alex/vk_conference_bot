TOKEN = ''
GROUP_ID = 

INTENTS = [
    {
        'name': 'Дата проведения',
        'tokens': ('когда', 'сколько', 'дата', 'дату'),
        'scenario': None,
        'answer': 'Конференция проводится 15-го апреля, регистрация начнёться в 10 утра'
    },
    {
        'name': 'Место проведения',
        'tokens': ('где', 'место', 'локация', 'адрес', 'метро'),
        'scenario': None,
        'answer': 'Конференция пройдёт в павльоне 18 Г в Экспоцентре'
    },
    {
        'name': 'Регистрация',
        'tokens': ('регист', 'добав'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            "step1": {
                'text': 'Чтобы зарегистрироваться, введите ваше имя. Оно будет написано на бэдже.',
                'failure_text': 'Имя должно состоять из 3-30 букв и дефиса. Попробуйте ещё раз',
                'handler': 'handle_name',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите email. Мы отправим нанего все данные',
                'failure_text': 'Во введённом адресе ошибка. Попроьуйте ешё раз',
                'handler': 'handle_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Спасибо за регистрацию, {name} ! Отправили вам билет ниже и'
                        ' отправили на {email} билет, распечайте его.',
                'image': 'generate_ticket_handler',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }
}

DEFAULT_ANSWER = 'Не знаю как на это ответить. ' \
                 'Могу сказать когда и где пройдёт конферениция, а так же зарегистрировать вас.'

DB_CONFIG = dict(
        provider='postgres',
        user='postgres',
        # password='1234',
        database='mydb',
        host='localhost'

)
