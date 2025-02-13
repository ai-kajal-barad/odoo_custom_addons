#-*- coding: utf-8 -*-
from odoo import models, fields

class Library(models.Model):
    """This class contain library related details."""
    _name = 'library.library'
    _description = "This is the library class."

    name=fields.Char(string='Book Title')
    location=fields.Char(string='Location')
    capacity=fields.Integer(string='Capacity')
    notes=fields.Text(string=' notes')
    product_ids = fields.Many2many(string='Products',comodel_name='product.template')
    member_id=fields.Many2one(comodel_name='library.member')
