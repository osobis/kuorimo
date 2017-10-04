#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import iter_db_results
from text_wrap import wrap_product


def show_products(d, size=20):
    cursor = d.get_cursor()
    db_result = cursor.execute("""SELECT * FROM product ORDER by number ASC""")
    iter_db_results(db_result, size, wrap_func=wrap_product)
    cursor.close()


def get_products(d):
    cursor = d.get_cursor()
    db_result = cursor.execute("""SELECT * FROM product ORDER by name ASC""")
    r = list(db_result)
    cursor.close()
    return r


def show_product(d, number):
    cursor = d.get_cursor()
    db_result = cursor.execute("SELECT * FROM product WHERE number=?", (number,))
    count = iter_db_results(db_result, 1, wrap_func=wrap_product)
    cursor.close()
    return count


def get_product_name(d, number):
    cursor = d.get_cursor()
    db_result = cursor.execute("SELECT name FROM product WHERE number=?", (number,))
    name = db_result.fetchone().get('name').encode('utf8')
    cursor.close()
    return name


def insert_product(d, product_number, product_name):
    cursor = d.get_cursor()
    cursor.execute("INSERT INTO product VALUES (?,?)", (product_number, product_name.decode('utf-8')))
    cursor.close()
    d.commit()


def edit_product_by_number(d, product_number, product_name):
    cursor = d.get_cursor()
    cursor.execute("UPDATE product SET name=? WHERE number=?", (product_name.decode('utf-8'), product_number))
    cursor.close()
    d.commit()


def delete_product_by_number(d, product_number):
    cursor = d.get_cursor()
    cursor.execute("DELETE FROM product WHERE number=?", (product_number, ))
    cursor.close()
    d.commit()
