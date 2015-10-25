import unittest
import os
from os import path
from askme.provider import Provider


def generate_provider(options):
    data_file = path.join(os.path.dirname(os.path.abspath(__file__)), '../../source/data/aws.json')
    return Provider(data_file, options)


class TestProvider(unittest.TestCase):

    def setUp(self):
        self.data = [{
            "id": "a",
            "desc": "a"
        }, {
            "id": "b",
            "desc": "bb"
        }, {
            "id": "cc",
            "desc": "ccc"
        }]

        self.columns = ["id", "desc"]

    def test_generate_cells_length(self):
        options = {
            'delimiter': None,
            'omit_columns': None,
            'fields': None
        }

        provider = generate_provider(options)
        ret = provider.generate_cells_length(self.data, self.columns)
        self.assertEquals(ret['id'], 2)
        self.assertEquals(ret['desc'], 3)

    def test_generate_row_output_with_default_output(self):
        options = {
            'delimiter': " | ",
            'omit_columns': None,
            'fields': None
        }

        provider = generate_provider(options)
        cells_length = provider.generate_cells_length(self.data, self.columns)
        ret = provider.generate_row_output(self.data[0], self.columns, cells_length)
        self.assertEquals(ret, "Id: a  | Description: a  ")

        ret = provider.generate_row_output(self.data[1], self.columns, cells_length)
        self.assertEquals(ret, "Id: b  | Description: bb ")

        ret = provider.generate_row_output(self.data[2], self.columns, cells_length)
        self.assertEquals(ret, "Id: cc | Description: ccc")

    def test_generate_row_output_without_column(self):
        options = {
            'delimiter': " || ",
            'omit_columns': True,
            'fields': None
        }

        provider = generate_provider(options)
        cells_length = provider.generate_cells_length(self.data, self.columns)
        ret = provider.generate_row_output(self.data[0], self.columns, cells_length)
        self.assertEquals(ret, "a  || a  ")

        ret = provider.generate_row_output(self.data[1], self.columns, cells_length)
        self.assertEquals(ret, "b  || bb ")

        ret = provider.generate_row_output(self.data[2], self.columns, cells_length)
        self.assertEquals(ret, "cc || ccc")

    def test_generate_row_output_with_selected_columns(self):
        new_columns = ['id']
        options = {
            'delimiter': " | ",
            'omit_columns': None,
            'fields': new_columns
        }

        provider = generate_provider(options)
        cells_length = provider.generate_cells_length(self.data, new_columns)
        ret = provider.generate_row_output(self.data[0], new_columns, cells_length)
        self.assertEquals(ret, "Id: a ")

        ret = provider.generate_row_output(self.data[1], new_columns, cells_length)
        self.assertEquals(ret, "Id: b ")

        ret = provider.generate_row_output(self.data[2], new_columns, cells_length)
        self.assertEquals(ret, "Id: cc")
