# -*- coding: utf-8 -*-
from openerp import api, models, fields, exceptions

class ProductCustom(models.Model):
    _name = 'product.custom'

    name = fields.Char('Product Name', required=True)
    description = fields.Text('Product Description')
    price = fields.Float('Product Price', required=True)
    image = fields.Binary('Product Image')


class ProductPurchase(models.Model):
    _name = 'product.purchase'

    product_id = fields.Many2one('product.custom', string='Product', required=True)
    # price = fields.Float('Product Price', related='product_id.price', readonly=True)
    buyer_amount = fields.Float('Buyer Amount',related='product_id.price', required=True)
    change = fields.Float('Change', compute='_compute_change', store=True)
    payment_status = fields.Selection([
        ('bayar', 'Bayar'),
        ('belum_bayar', 'Belum Bayar'),
        ('lunas', 'Lunas'),
        ('belum_lunas', 'Belum Lunas')
    ], string='Payment Status', default='belum_bayar')
    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ], string='Approval State', default='draft')

    @api.depends('buyer_amount', 'product_id.price')
    def _compute_change(self):
        for record in self:
            record.change = record.buyer_amount - record.product_id.price if record.buyer_amount > record.product_id.price else 0.0

    @api.onchange('payment_status')
    def _onchange_payment_status(self):
        # When Payment Status is 'Lunas' or 'Belum Lunas', allow the button to be clickable and set approval state to draft
        if self.payment_status in ['lunas', 'belum_lunas']:
            self.approval_state = 'draft'

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        # Confirm when the payment status is either 'Lunas' or 'Belum Lunas'
        if self.payment_status in ['lunas', 'belum_lunas'] and self.approval_state == 'draft':
            self.approval_state = 'confirmed'
        else:
            raise exceptions.Warning('Cannot confirm without a valid payment status.')

    @api.multi
    def action_reject(self):
        self.ensure_one()
        self.approval_state = 'rejected'
