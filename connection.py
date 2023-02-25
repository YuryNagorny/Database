import sqlite3
import DB_Parking
import main
import QR
from werkzeug.security import (check_password_hash, generate_password_hash)

db = sqlite3.connect("base.db")

#БЛОК ФУНКЦИЙ ДЛЯ ВЛАДЕЛЬЦА
def OWNER_reg(login, psw):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `email_adress` FROM `OWNER_data_base` WHERE `login` = '{login}'
        '''
    )
    res = cur.fetchall()
    db.commit()
    if len(res) == 0:
        cur.execute(
            f'''
                INSERT INTO `OWNER_data_base`(`email_adress`, `password`)
                VALUES (
                    '{login}',
                    '{generate_password_hash(psw)}'
                )
            '''
        )
        db.commit()
        return {
            "msg": "Вы успешно зарегистрировались!",
            "status": True,
            "id": get_OWNER_id(login)["id"]
        }
    return {
        "msg": "Такой e-mail уже зарегистрирован!",
        "status": False
    }


def get_OWNER_id(login):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(
        f'''
            SELECT `id` FROM `OWNER_data_base` WHERE `email_adress` = '{login}'
        '''
    )
    res = cur.fetchall()
    db.commit()
    return {
        "id": res[0]["id"]
    }


def OWNER_log(login, psw):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f'''SELECT `id`, `email_adress`, `password` FROM `OWNER_data_base`''')
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row['email_adress'] == login and check_password_hash(
            row['password'],
            psw
        ):
            return {
                "msg": "Вы успешно вошли",
                "status": True,
                "id": row["id"]
            }
    else:
        return {
            "msg": "Неверный логин/пароль!",
            "status": False
        }


def owner_chek_psw(user_id, psw):
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute(f'''SELECT `id`, `password` FROM `OWNER_data_base`''')
    res = cur.fetchall()
    db.commit()
    for row in res:
        if row["id"] == int(user_id) and check_password_hash(
            row["password"],
            psw
        ):
            return {
                "msg": "Пароли совпали",
                "status": True,
            }
    else:
        return {
            "msg": "Пароли не совпали",
            "status": False
        }
    
#БЛОК ФУНКЦИЙ ДЛЯ ПАРКИНГОВ