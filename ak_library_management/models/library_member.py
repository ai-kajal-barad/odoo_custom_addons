#-*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryMember(models.Model):
    """This class have members details like name
    contact details and membership date."""
    _name = 'library.member'
    _description = ("This is the member class for "
                    "managing the members")

    name=fields.Char(string='Member Name')
    email=fields.Char(string='Email ID')
    phone=fields.Char(string='Contact Number')
    membership_date=fields.Date(string='Membership Start Date')
    library_ids=fields.One2many(comodel_name='library.library', inverse_name='member_id')
