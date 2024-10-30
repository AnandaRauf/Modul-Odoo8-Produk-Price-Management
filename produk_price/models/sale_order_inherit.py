from openerp import api, models, fields
from openerp.exceptions import MissingError

class SaleOrderLine(models.Model):  
    _inherit = 'sale.order.line'

    product_id = fields.Many2one(
        'product.custom', string='Product', required=True,
        domain=[('state', 'in', ['confirmed', 'approved'])]
    )
    
    price_unit = fields.Float(
        string='Price Unit',
        related='product_id.price',  # Pulls price from `product.custom`
        store=True,
        readonly=True
    )

    @api.onchange('product_id', 'price_unit')
    def _onchange_product_id(self):
        if not self.product_id:
            self.price_unit = 0
        else:
            try:
                self.price_unit = self.product_id.price
            except MissingError:
                self.product_id = False
                self.price_unit = 0

    
    # quantity = fields.Integer('Quantity', required=True, default=1)
    # total_price = fields.Float(
    #     string='Total Price',
    #     compute='_compute_total_price',
    #     store=True
    # )
    #
    # @api.depends('price_unit', 'quantity')
    # def _compute_total_price(self):
    #     for record in self:
    #         record.total_price = record.price_unit * record.quantity
