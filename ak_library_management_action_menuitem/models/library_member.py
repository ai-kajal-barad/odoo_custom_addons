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
    # borrow_book_count=fields.Integer(string='Borrowed Book', compute='_compute_book_count')
    #
    # @api.depends(id)
    # def _compute_book_count(self):
    #     borrow=self.env['library.library']
    #     for rec in self:
    #         rec.borrow_book_count=len(id)

    def action_view_borrow_book(self):
        self.ensure_one()
        return {
            'name':'Borrowed Book',
            'type':'ir.actions.act_window',
            'res_model':'library.library',
            'view_mode':'list,form',
            'domain':[('member_id','=',self.id)],
            'context':{'default_member_id':self.id}
        }