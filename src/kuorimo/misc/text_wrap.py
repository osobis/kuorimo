#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Table(object):
    def __init__(self, *columns):
        self.columns = columns
        self.length = max(len(col.data) for col in columns)

    def get_row(self, row_num=None):
        for col in self.columns:
            if row_num is None:
                yield col.format % col.name
            else:
                value = col.data[row_num]
                yield col.format % value

    def get_line(self):
        for col in self.columns:
            yield '-' * (col.width + 2)

    @staticmethod
    def join_n_wrap(char, elements):
        return ' ' + char + char.join([element.encode('utf-8') for element in elements]) + char

    @property
    def get_rows(self):
        yield self.join_n_wrap('+', self.get_line())
        yield self.join_n_wrap('|', self.get_row(None))
        yield self.join_n_wrap('+', self.get_line())
        for row_num in range(0, self.length):
            yield self.join_n_wrap('|', self.get_row(row_num))
        yield self.join_n_wrap('+', self.get_line())

    def __str__(self):
        return '\n'.join(self.get_rows)

    class Column:
        LEFT, RIGHT = '-', ''

        def __init__(self, name, data, align=RIGHT):
            self.data = data
            self.name = name
            self.width = max(len(x) for x in data + [name])
            self.format = ' %%%s%ds ' % (align, self.width)

def wrap_customer(results):
    numbers = []
    names = []
    for result in results:
        numbers.append(str(result['number']))
        names.append(result['name'])
    column = Table.Column
    print Table(
        column('No', numbers),
        column('Customer', names, align=column.LEFT)
    )


def wrap_product(results):
    numbers = []
    names = []
    for result in results:
        numbers.append(str(result['number']))
        names.append(result['name'])
    column = Table.Column
    print Table(
        column('No', numbers),
        column('Product', names, align=column.LEFT)
    )


def wrap_order(results):
    order_ids = []
    order_dates = []
    customer_names = []
    product_names = []
    order_amounts = []
    for result in results:
        order_ids.append(str(result['order_id']))
        order_dates.append(result['order_date'])
        customer_names.append(result['customer_name'])
        product_names.append(result['product_name'])
        order_amounts.append(str(result['order_amount']))
    column = Table.Column
    print Table(
        column('Order ID', order_ids),
        column('Date', order_dates),
        column('Customer', customer_names, align=column.LEFT),
        column('Product', product_names, align=column.LEFT),
        column('Amount', order_amounts, align=column.RIGHT)
    )


if __name__ == '__main__':

    Column = Table.Column
    nums = [ '1', '2', '3', '4' ]
    speeds = [ '100', '10000', '1500', '12' ]
    desc = [ '', 'label 1', 'none', u'very long descriptiona a aaaaaaaa' ]
    print Table(
        Column('NUM', nums),
        Column('SPEED', speeds),
        Column('DESC', desc, align=Column.LEFT))