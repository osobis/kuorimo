#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from database import iter_db_results
from text_wrap import wrap_order


def show_orders(d, year=None, month=None, size=20):
    cursor = d.get_cursor()
    today = datetime.today()
    year = str(year or today.year)
    month = str(month or today.month).zfill(2)

    query = """SELECT 
                orders.id as order_id,
                orders.date as order_date,
                customer.name as customer_name,
                product.name as product_name,
                orders.amount as order_amount
                FROM orders 
                JOIN customer ON orders.cust_number=customer.number
                JOIN product ON orders.prod_number = product.number
                WHERE strftime('%Y%m', orders.date) = ?
                ORDER BY orders.id DESC
                """
    date = year + month
    db_result = cursor.execute(query, (date, ))
    print 'Showing orders for {}-{}'.format(year, month)
    iter_db_results(db_result, size, wrap_func=wrap_order)
    cursor.close()


def show_order(d, order_id):
    cursor = d.get_cursor()

    query = """SELECT 
                orders.id as order_id,
                orders.date as order_date,
                customer.name as customer_name,
                product.name as product_name,
                orders.amount as order_amount
                FROM orders 
                JOIN customer ON orders.cust_number=customer.number
                JOIN product ON orders.prod_number = product.number
                WHERE orders.id=?
                """
    db_result = cursor.execute(query, (order_id, ))
    count = iter_db_results(db_result, 1, wrap_func=wrap_order)
    cursor.close()
    return count


def insert_order(d, date, customer_number, product_number, amount):
    cursor = d.get_cursor()
    cursor.execute("INSERT INTO orders (cust_number, prod_number, amount, date) VALUES (?, ?, ?, ?)",
                   (customer_number, product_number, amount, date))
    cursor.close()
    d.commit()


def delete_order_by_id(d, order_id):
    cursor = d.get_cursor()
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id, ))
    cursor.close()
    d.commit()
