# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderWizard(models.TransientModel):
    """
    create transient model and add message field to show the wizard message
    """
    _name = 'sale.order.wizard'
    _description = 'Sale order wizard'

    message = fields.Char(readonly=True)
