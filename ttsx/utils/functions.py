import random


def random_session():
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    session = ''
    for i in range(50):
        session += random.choice(s)
    return session


def random_order():
    s = '1234567890'
    order = ''
    for i in range(15):
        order += random.choice(s)
    return order