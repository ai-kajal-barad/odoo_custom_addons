#-*- coding: utf-8 -*-
from odoo import models, fields, api

class LibraryMember(models.Model):
    """This class have members details like name
    contact details and membership date."""
    _name = 'library.member'
    _description = "This is the member class for managing the members"

    name=fields.Char(string='Member Name')
    email=fields.Char(string='Email ID')
    phone=fields.Char(string='Contact Number')
    membership_date=fields.Date(string='Membership Start Date')
    borrow_book_count=fields.Char(string='Borrowed Book', compute='_compute_book_count')
    library_ids=fields.One2many(comodel_name='library.library', inverse_name='member_id')

    @api.depends('library_ids')
    def _compute_book_count(self):
        """count books"""
        for member in self:
            member.borrow_book_count=len(member.library_ids)

    def action_view_borrow_book(self):
        """method for smart button"""
        self.ensure_one()
        return {
            'name':'Borrowed Book',
            'type':'ir.actions.act_window',
            'res_model':'library.library',
            'view_mode':'list,form',
            'domain':[('member_id','=',self.id)],
            'context':{'default_member_id':self.id}
        }
