from openerp import api, models, fields
from openerp.exceptions import AccessError

class SaleOrderDates(models.Model):  
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(
        'product.custom', string='Product', required=True,
        domain=[('state', 'in', ['confirmed', 'approved'])]
    )
    
    price_unit = fields.Float(
        string='Price Unit',
        related='product_id.price',  # Mengambil harga dari `product.custom`
        store=True,
        readonly=True
    )

    quantity = fields.Integer('Quantity', required=True, default=1)
    
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True
    )

    @api.depends('price_unit', 'quantity')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.price_unit * record.quantity
