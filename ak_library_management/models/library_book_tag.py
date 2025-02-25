#-*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBookTag(models.Model):
    """This class contain book Tags."""
    _name = 'library.book.tag'
    _description = "This is the books class for managing the books"

    name=fields.Char(string='Book Tags')
