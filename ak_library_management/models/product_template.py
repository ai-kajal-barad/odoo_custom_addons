#-*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_library_book=fields.Boolean(string='Is Library Book')
    author=fields.Char(string='Author Name')
    publisher=fields.Char(string='Publisher')
    edition=fields.Char(string='Edition')
    published_date=fields.Date(string='Date of Publication')
    pages=fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    barcode = fields.Char(string="ISBN Number")
