#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unicodedata
from collections import defaultdict
from string import ascii_uppercase

import xlsxwriter
from database import Database

from customer import get_customers_by_number
from product import get_products


def get_report(d, customer_number, year, month):
    cursor = d.get_cursor()
    query = """ SELECT  orders.date AS order_date,
                product.name AS product_name,
                product.number AS product_number, SUM(orders.amount) AS total
                FROM orders 
                JOIN product ON orders.prod_number=product.number
                WHERE orders.cust_number=? AND strftime('%Y%m', orders.date)=?
                GROUP BY orders.prod_number, orders.date
                ORDER by orders.date, product.name"""

    results = defaultdict(list)
    period = year + str(month).zfill(2)
    db_result = cursor.execute(query, (customer_number, period))
    for item in db_result:
        results[item['order_date']].append((item['product_number'], item['total']))
    cursor.close()
    return results


class XlsReportGenerator(object):
    """Generate xls report, each customer in its own worksheet"""

    def __init__(self, year, month, path_to_report):
        self.month = month
        self.year = str(year)
        self.db = Database()
        self.workbook = xlsxwriter.Workbook(path_to_report)
        # Add formats to use to highlight cells.
        self.bold = self.workbook.add_format({'bold': True})
        self.bold_red = self.workbook.add_format({'bold': True, 'font_color': 'red'})
        self.bold_sized = self.workbook.add_format({'bold': True, 'font_size': 14})
        self.bold_bg_gray = self.workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'gray'})
        self.bold_bg_gray_sized = self.workbook.add_format({'bold': True,
                                                            'font_color': 'white',
                                                            'font_size': 13,
                                                            'bg_color': 'gray'})

        # Create a format to use in the merged range.
        self.merge_format = self.workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})

        self.worksheets = {}
        self.customers = {}
        self.products = {}

    def generate_workbook(self):
        for customer in get_customers_by_number(self.db):
            customer_name = unicodedata.normalize('NFD', customer['name']).encode('ascii', 'ignore')
            customer_name = customer_name.replace('/', '_')
            customer_name = customer_name.replace('?', '_')
            customer_name = customer_name.replace('*', '_')
            customer_name = customer_name.replace(':', '_')
            customer_number = customer['number']
            self.customers[customer_number] = customer_name
            worksheet = self.workbook.add_worksheet(str(customer_number))
            worksheet.set_column('A:A', 12)
            worksheet.write('A3', 'Date', self.bold_bg_gray)
            for product, cell_letter in zip(get_products(self.db), ascii_uppercase[1:]):
                worksheet.set_column('%s:%s' % (cell_letter, cell_letter), 13)
                worksheet.write(cell_letter + '3', product['name'], self.bold_bg_gray)
                self.products[product['number']] = cell_letter

            self.worksheets[customer['number']] = worksheet

    def generate_worksheet(self, customer_number, customer_name):
        reports = get_report(self.db, customer_number, self.year, self.month)
        dates = sorted(reports.keys())

        # print the name of the customer to be able to generate PDF file
        customer_text = "{}/{}".format(customer_number, customer_name)
        self.worksheets[customer_number].merge_range('A1:F1', customer_text, self.merge_format)

        cell_number = 4
        for date in dates:
            date_cell = 'A' + str(cell_number)
            self.worksheets[customer_number].write(date_cell, date)
            rows = reports[date]
            for product_number, total in rows:
                product_cell = self.products[product_number] + str(cell_number)
                self.worksheets[customer_number].write(product_cell, total)
                self.worksheets[customer_number].write(product_cell, total)
            cell_number += 1

        if reports:
            self.worksheets[customer_number].write('A' + str(cell_number + 2), 'Total', self.bold_bg_gray_sized)
            for cell_letter in ascii_uppercase[1: len(self.products) + 1]:
                self.worksheets[customer_number].write(cell_letter + str(cell_number + 2),
                                                       '=SUM(%s:%s)' % (cell_letter + '2',
                                                                        cell_letter + str(cell_number - 1)),
                                                       self.bold_bg_gray_sized)

    def generate_report(self):
        self.generate_workbook()
        for customer_number, customer_name in self.customers.items():
            self.generate_worksheet(customer_number, customer_name)
        self.workbook.close()


def generate_report(year, month, path):
    g = XlsReportGenerator(year, month, path)
    g.generate_report()
    return os.path.exists(path)


if __name__ == '__main__':
    generate_report(2017, 9, '/Users/skocle/Desktop/demo.xlsx')
