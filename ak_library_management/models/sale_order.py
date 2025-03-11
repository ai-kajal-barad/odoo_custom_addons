# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    """
    Inherit sale_order model and add some buttons on base of some conditions.
    """
    _inherit = 'sale.order'

    is_check = fields.Boolean()
    is_approve = fields.Boolean()

    def action_confirm(self):
        """
        Confirm the given quotation(s) if stock is grater than 5
        otherwise generate validation popup

        :return: True or custom wizard
        :rtype: bool or dictionary
        """
        low_stock_products = []
        for record in self.order_line:
            if record.product_template_id.qty_available < 5:
                low_stock_products.append(record.product_template_id.name)

        if low_stock_products and not self.is_approve:
            self.is_check = True
            message = ("Approval needed! The following books have low stock:"
                       + ','.join(low_stock_products))
            return {
                'name': 'Sale Order Warning',
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_message': message}
            }
        return super().action_confirm()

    def action_approve(self):
        """
        check the current user is manager or not
        if manager than approve is true and confirm is false and only manager is Enable this button
        """
        if self.env.user.is_manager:
            self.is_check = False
            self.is_approve = True

    def action_reject(self):
        """
        user can reject the quotation(s)
        """
        self.is_check = False
        self.action_cancel()

    def action_cancel(self):
        """
        cancel the quotation(s) and False is_approve
        """
        if self.is_approve:
            self.is_approve = False
        return super().action_cancel()
