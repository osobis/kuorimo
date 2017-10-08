#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from functools import wraps
from os.path import expanduser

import dateutil.parser
from cursesmenu import *
from cursesmenu.items import *

from customer import (show_customers, insert_customer, show_customer,
                      edit_customer_by_number, get_customer_name, get_customers)
from database import Database
from order import show_orders, insert_order, show_order, delete_order_by_id
from product import show_products, show_product, get_product_name, edit_product_by_number, insert_product, get_products
from report import generate_report


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def press_enter(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        r = f(*args, **kwargs)
        raw_input("Press ENTER to return to Menu")
        return r
    return wrapped


@press_enter
def not_implemented(text):
    print text + ' ' + 'not yet implemented'


@press_enter
def print_products(d, size):
    show_products(d, size)


@press_enter
def print_customers(d, size):
    show_customers(d, size)


@press_enter
def print_orders(d, size):
    today = datetime.today()
    year = raw_input('Enter year (YYYY/default: {}): '.format(str(today.year)))
    month = raw_input('Enter month (MM/default: {}): '.format(str(today.month).zfill(2)))
    show_orders(d, year, month, size)


@press_enter
def add_order(d):
    order_date = ''
    while True:
        if not order_date:
            default_order_date = str(datetime.today().date())
            order_date = raw_input('Date [{}]: '.format(default_order_date))
            if not order_date:
                order_date = default_order_date
            order_date = dateutil.parser.parse(order_date).date()
            order_date = str(order_date)
        else:
            input_str = 'Date [{}]: '.format(order_date)
            new_date = raw_input(input_str)
            if new_date:
                order_date = str(dateutil.parser.parse(new_date).date())
        customer_number = raw_input('Customer Number: ')
        product_number = raw_input('Product Number: ')
        amount = raw_input('Amount: ')
        try:
            customer_name = get_customer_name(d, customer_number)
            product_name = get_product_name(d, product_number)
        except Exception, err:
            print ("ERROR: Failed to fetch customer/product details. Error: ", str(err))
            continue
        print
        print 'CONFIRM: **', order_date, '**',
        print customer_name, '**',
        print product_name, '**',
        print amount + 'kg **'
        print
        confirmation = raw_input('(Y/N/Q/S=Save and Quit): ')
        if confirmation in ('Y', 'y', '', 's', 'S'):
            try:
                insert_order(d, order_date, customer_number, product_number, amount)
                print ("= ORDER SAVED =")
            except Exception, err:
                print ("ERROR: Failed to add order. Error: ", str(err))
            if confirmation in ('s', 'S'):
                break
            print
        elif confirmation in ('Q', 'q', 'quit'):
            print ("= ORDER ENTRY QUIT. RETURNING TO MAIN MENU =")
            break
        elif confirmation in ('N', 'n'):
            print ("= ORDER IGNORED =")


@press_enter
def remove_order(d):
    order_id = raw_input("Order id: ")
    result = show_order(d, order_id)
    if not result:
        print "No order with id {}".format(order_id)
        return
    confirmation = raw_input('Confirm delete (Y/N): ')
    if confirmation in ('Y', 'y'):
        delete_order_by_id(d, order_id)
        print "ORDER DELETED"
    else:
        print "ORDER HAS NOT BEEN DELETED"


@press_enter
def add_customer(d):
    number = raw_input("Customer number: ")
    name = raw_input("Customer name: ")
    try:
        insert_customer(d, number, name)
        show_customer(d, number)
    except Exception, err:
        print ("ERROR: Failed to add customer. Error: ", str(err))


@press_enter
def modify_customer(d):
    number = raw_input("Customer number: ")
    result = show_customer(d, number)
    if not result:
        print "No customer with number {}".format(number)
        return
    name = raw_input("New customer name: ")
    if name:
        edit_customer_by_number(d, number, name)
    show_customer(d, number)


@press_enter
def add_product(d):
    number = raw_input("Product number: ")
    name = raw_input("Product name: ")
    try:
        insert_product(d, number, name)
        show_product(d, number)
    except Exception, err:
        print ("ERROR: Failed to add product. Error: ", str(err))


@press_enter
def modify_product(d):
    number = raw_input("Product number: ")
    result = show_product(d, number)
    if not result:
        print "No product with number {}".format(number)
        return
    name = raw_input("New product name: ")
    if name:
        edit_product_by_number(d, number, name)
    show_product(d, number)


@press_enter
def generate_monthly_report():

    home_dir = expanduser("~")
    print 'To generate the xls report please specify the following:'
    year = raw_input('Enter year (YYYY): ')
    month = raw_input('Enter month (MM): ')
    path = os.path.join(home_dir, "{}-{}.xlsx".format(year, month.zfill(2)))
    try:
        if generate_report(year, month, path):
            print 'Report can be found at {}'.format(path)
    except Exception, err:
        print ("ERROR: Failed to create report. Error: ", str(err))


@press_enter
def generate_customers_list(d):
    home_dir = expanduser("~")
    path = os.path.join(home_dir, 'kuorimo_customers.txt')
    with open(path, 'w') as fp:
        fp.write("Customers List\n")
        fp.write("=========================\n\n")
        for customer in get_customers(d):
            fp.write(str(customer['number']).rjust(2) + '. ' + customer['name'].encode('utf-8') + '\n')
    print 'Customers list can be found at {}'.format(path)


@press_enter
def generate_products_list(d):
    home_dir = expanduser("~")
    path = os.path.join(home_dir, 'kuorimo_products.txt')
    with open(path, 'w') as fp:
        fp.write("Products List\n")
        fp.write("=========================\n\n")
        for customer in get_products(d):
            fp.write(str(customer['number']).rjust(2) + '. ' + customer['name'].encode('utf-8') + '\n')
    print 'Products list can be found at {}'.format(path)


def menu():

    create_dir(os.path.join(expanduser("~"), 'kuorimo_data'))

    d = Database()

    main_menu = CursesMenu("KUORIMO OY")

    # Customers
    customers_menu = CursesMenu("Customers")

    customers_menu.append_item(FunctionItem("Show customers", print_customers, [d, 20]))
    customers_menu.append_item(FunctionItem("Add customer", add_customer, [d]))
    customers_menu.append_item(FunctionItem("Edit customer", modify_customer, [d]))
    customers_menu.append_item(FunctionItem("Generate customers list", generate_customers_list, [d]))

    customers_submenu_item = SubmenuItem("Customers", submenu=customers_menu)
    customers_submenu_item.set_menu(main_menu)

    # Products
    products_menu = CursesMenu("Products")

    products_menu.append_item(FunctionItem("Show products", print_products, [d, 20]))
    products_menu.append_item(FunctionItem("Add product", add_product, [d]))
    products_menu.append_item(FunctionItem("Edit product", modify_product, [d]))
    products_menu.append_item(FunctionItem("Generate products list", generate_products_list, [d]))

    products_submenu_item = SubmenuItem("Products", submenu=products_menu)
    products_submenu_item.set_menu(main_menu)

    # Orders
    orders_menu = CursesMenu("Orders")

    orders_menu.append_item(FunctionItem("Add order", add_order, [d]))
    orders_menu.append_item(FunctionItem("Show orders", print_orders, [d, 20]))
    orders_menu.append_item(FunctionItem("Delete order", remove_order, [d]))

    orders_submenu_item = SubmenuItem("Orders", submenu=orders_menu)
    orders_submenu_item.set_menu(main_menu)

    # Reports
    reports_menu = CursesMenu("Reports")

    reports_menu.append_item(FunctionItem("Generate daily report", not_implemented, ['Daily report']))
    reports_menu.append_item(FunctionItem("Generate monthly report", generate_monthly_report))
    reports_menu.append_item(FunctionItem("Generate yearly report", not_implemented, ['Yearly report']))

    reports_submenu_item = SubmenuItem("Reports", submenu=reports_menu)
    reports_submenu_item.set_menu(main_menu)

    main_menu.append_item(orders_submenu_item)
    main_menu.append_item(customers_submenu_item)
    main_menu.append_item(products_submenu_item)
    main_menu.append_item(reports_submenu_item)
    main_menu.start()
    main_menu.join()


if __name__ == '__main__':
    menu()