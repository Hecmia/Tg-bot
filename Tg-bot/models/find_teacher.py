import sqlite3
import json
connection = sqlite3.connect('C:/Users/Алиса/PycharmProjects/Tg-bot/database/database.db')
cursor = connection.cursor()

def find_teacher_by_full_name(name):
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ?', (f'%{name}%',))
    results = cursor.fetchall()
    return results


def find_teacher_by_department(department):
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ?', (f'%{department}%',))
    results = cursor.fetchall()
    return results


def find_teacher_by_group_and_department(department, group):
    cursor.execute('SELECT name, department FROM teachers WHERE department LIKE ? AND groups LIKE ?',
                   (f'%{department}%', f'%{group}%',))
    results = cursor.fetchall()
    return results


def find_by_name_and_department(name, department):
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ? AND name LIKE ?', (f'%{department}%', f'%{name}%', ))
    results = cursor.fetchall()
    return results


def find_by_department_and_subject(department, subject):
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ? AND subjects LIKE ?',
                   (f'%{department}%', f'%{subject}%',))
    results = cursor.fetchall()
    return results


def find_by_department_name_subject(name, department, subject):
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND department LIKE ? AND subjects LIKE ?',
                   (f'%{name}%', f'%{department}%', f'%{subject}%',))
    results = cursor.fetchall()
    return results


def find_subject(subject):
    cursor.execute('SELECT name FROM teachers WHERE subjects LIKE ?', (f'%{subject}%',))
    results = cursor.fetchall()
    return results


def find_by_name_and_subject(name, subject):
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND subjects LIKE ?',
                   (f'%{name}%', f'%{subject}%'))
    results = cursor.fetchall()
    return results


def find_search_by_group_and_subject(group, subject):
    cursor.execute('SELECT name, department FROM teachers WHERE groups LIKE ? AND subjects LIKE ?',
                   (f'%{group}%', f'%{subject}%'))
    results = cursor.fetchall()
    return results


def find_by_full_name_and_subject(full_name, subjects, group):
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND groups LIKE ? AND subjects LIKE ?',
                   (f'%{full_name}%', f'%{group}%',
                    f'%{subjects}%',))
    results = cursor.fetchall()
    return results


def find_by_group(group):
    cursor.execute('SELECT name FROM teachers WHERE groups LIKE ?', (f'%{group}%',))
    results = cursor.fetchall()
    return results



def find_by_department_and_group_and_full_name(full_name, department, group):
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND groups LIKE ? AND department LIKE ?',
                   (f'%{full_name}%', f'%{group}%',
                    f'%{department}%',))
    results = cursor.fetchall()
    return results


def find_by_subject_and_group_and_name(full_name, group, subject):
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND groups LIKE ? AND subjects LIKE ?',
                   (f'%{full_name}%', f'%{group}%',
                    f'%{subject}%',))
    results = cursor.fetchall()
    return results


def find_by_name_and_group(name, group):
    cursor.execute('SELECT name FROM teachers WHERE groups LIKE ? AND name LIKE ?',
                   (f'%{group}%', f'%{name}%',))
    results = cursor.fetchall()
    return results



