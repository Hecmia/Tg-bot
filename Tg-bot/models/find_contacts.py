import sqlite3
import json
connection = sqlite3.connect('C:/Users/Алиса/PycharmProjects/Tg-bot/database/database.db')
cursor = connection.cursor()


def create_normal_day(day):
    if day == "ПН":
        selected_day = "Понедельник"
    elif day == "ВТ":
        selected_day = "Вторник"
    elif day == "СР":
        selected_day = "Среда"
    elif day == "ЧТ":
        selected_day = "Четверг"
    elif day == "ПТ":
        selected_day = "Пятница"
    elif day == "СБ":
        selected_day = "Суббота"
    return selected_day


def find_day(name):
    cursor.execute('SELECT name, rasp FROM teachers WHERE name LIKE ?',
                   (f'%{name}%',))
    results = cursor.fetchall()
    return results


def find_full_week(name):
    cursor.execute('SELECT name, rasp FROM teachers WHERE name LIKE ?',
                   (f'%{name}%',))
    results = cursor.fetchall()
    return results


def find_week1(name):
    cursor.execute('SELECT name, rasp FROM teachers WHERE name LIKE ?',
                   (f'%{name}%',))
    results = cursor.fetchall()
    return results


def find_week2(name):
    cursor.execute('SELECT name, rasp FROM teachers WHERE name LIKE ?',
                   (f'%{name}%',))
    results = cursor.fetchall()
    return results


def find_contacts(name):
    cursor.execute('SELECT name, contacts, department FROM teachers WHERE name LIKE ?',
                   (f'%{name}%',))
    results = cursor.fetchall()
    return results

