#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

# use those paths as valid paths to the database
DATABASE_PATHS = ['/Users/skocle/kuorimo.db',
                  '/Users/kirstikoivula/kuorimo.db',
                  r'C:\kuorimo\kuorimo.db']


def iter_db_results(db_result, size, wrap_func):
    count = 0
    while True:
        results = db_result.fetchmany(size=size)
        if not results:
            break
        elif count > 0:
            raw_input("== Press ENTER for more ==")

        wrap_func(results)

        count += 1
    return count


class Database(object):

    def __init__(self, db_name=None):

        self.db_name = db_name or self.get_db_path()
        self.conn = None

    @staticmethod
    def get_db_path():
        for path in DATABASE_PATHS:
            if os.path.exists(path):
                return path

    @staticmethod
    def _dict_factory(_cursor, row):
        """
        Allow result to be in the dict format
        @:param _cursor: database cursor
        @:param row: database row
        """
        d = {}
        for idx, col in enumerate(_cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_cursor(self, row_factory=None):

        if not self.conn:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

        cursor = self.conn.cursor()
        cursor.row_factory = row_factory or self._dict_factory

        return cursor

    def commit(self):
        if self.conn:
            self.conn.commit()
