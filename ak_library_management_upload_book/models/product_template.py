#-*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    """Inherited class using for books"""

    _inherit = 'product.template'

    author=fields.Char(string='Author Name')
    publisher=fields.Char(string='Publisher')
    edition=fields.Char(string='Edition')
    published_date=fields.Date(string='Date of Publication')
    pages=fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    isbn = fields.Char(string="ISBN Number")
    is_bulk_book=fields.Boolean(string='Is Bulk')
