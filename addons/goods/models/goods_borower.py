from odoo import models, fields

class GoodsBorower(models.Model):
    _name = 'goods.borower'
    _description = 'Goods Borower'

    name = fields.Char(string='Name', required=True)
