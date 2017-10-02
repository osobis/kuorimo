#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kuorimo.misc.database import Database, iter_db_results
from kuorimo.misc.text_wrap import wrap_customer


def show_customers(d, size=20):
    cursor = d.get_cursor()
    db_result = cursor.execute("""SELECT * FROM customer ORDER by number ASC""")
    iter_db_results(db_result, size, wrap_func=wrap_customer)
    cursor.close()


def get_customers(d):
    cursor = d.get_cursor()
    db_result = cursor.execute("""SELECT * FROM customer ORDER by name ASC""")
    r = list(db_result)
    cursor.close()
    return r


def show_customer(d, number):
    cursor = d.get_cursor()
    db_result = cursor.execute("SELECT * FROM customer WHERE number=?", (number, ))
    count = iter_db_results(db_result, 1, wrap_func=wrap_customer)
    cursor.close()
    return count


def get_customer_name(d, number):
    cursor = d.get_cursor()
    db_result = cursor.execute("SELECT name FROM customer WHERE number=?", (number,))
    name = db_result.fetchone().get('name').encode('utf8')
    cursor.close()
    return name


def insert_customer(d, customer_number, customer_name):
    cursor = d.get_cursor()
    cursor.execute("INSERT INTO customer VALUES (?,?)", (customer_number, customer_name.decode('utf-8')))
    cursor.close()
    d.commit()


def edit_customer_by_number(d, customer_number, customer_name):
    cursor = d.get_cursor()
    cursor.execute("UPDATE customer SET name=? WHERE number=?", (customer_name.decode('utf-8'), customer_number))
    cursor.close()
    d.commit()


def delete_customer_by_number(d, customer_number):
    cursor = d.get_cursor()
    cursor.execute("DELETE FROM customer WHERE number=?", (customer_number, ))
    cursor.close()
    d.commit()


if __name__ == '__main__':
    d = Database()

    insert_customer(d, 29, 'Pori')
    #delete_customer_by_number(d, 26)

    show_customers(d)




