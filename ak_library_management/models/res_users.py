#-*- coding: utf-8 -*-
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_manager = fields.Boolean(string="Is Manager", help="Allows user to approve/reject sale orders.")
