#-*- coding: utf-8 -*-
from odoo import models, fields
class Library(models.Model):
    _name = 'library.library'
    _description = "This is the books class for managing the books"

    name=fields.Char(string='Book Title')
    location=fields.Char(string='Location')
    isbn=fields.Char(string='ISBN Number')
    capacity=fields.Integer(string='Capacity')
    notes=fields.Text(string=' notes')
