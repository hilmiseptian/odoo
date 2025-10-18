from odoo import models, fields

class LibraryPartner(models.Model):
    _name = 'library.partner'
    _description = 'Library Partner'

    name = fields.Char(string='Name', required=True)
