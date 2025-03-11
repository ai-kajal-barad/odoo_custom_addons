# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class LibraryMember(models.Model):
    """This class have members details like name
    contact details and membership date."""
    _name = 'library.member'
    _description = "This is the member class for managing the members"

    name = fields.Char(string='Member Name')
    membership_no = fields.Char(string='Membership Number')
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    library_ids = fields.One2many(comodel_name='library.library', inverse_name='member_id')

    @api.model_create_multi
    def create(self, vals_list):
        """
        inherit the create method and update sequence number.
        """
        for val in vals_list:
            val['membership_no'] = self.env["ir.sequence"].next_by_code('library.member')
        return super().create(vals_list)