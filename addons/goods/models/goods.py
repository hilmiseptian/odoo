from odoo import models, fields, api, exceptions
from datetime import date, timedelta

class Goods(models.Model):
    _name = 'goods'
    _description = 'Goods Module'

    name = fields.Char(
        string='Name',
        required=True
    )
    created_by = fields.Char(
        string='Created By'
    )
    created_date = fields.Date(
        string='Created Date'
    )
    borrower_id = fields.Many2one(
        comodel_name='goods.borower',
        string='Borrower'
    )
    state = fields.Selection(
        [
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost'),
        ],
        string='State',
        default='available'
    )
    borrowed_date = fields.Date(
        string='Borrowed Date'
    )
    days_borrowed = fields.Integer(
        string='Days Borrowed',
        compute='_compute_days_borrowed',
        store=False
    )

    # 1. Button method untuk borrow
    def action_borrow(self):
        for record in self:
            if record.state in ['borrowed', 'lost']:
                raise exceptions.UserError('Barang ini tidak tersedia untuk dipinjam.')
            if not record.borrower_id:
                raise exceptions.UserError('Peminjam harus dipilih terlebih dahulu.')
            record.state = 'borrowed'
            record.borrowed_date = date.today()

    # 2. Button method untuk return
    def action_return(self):
        for record in self:
            record.state = 'available'
            record.borrower_id = False
            record.borrowed_date = False

    # 3. Computed field days_borrowed
    @api.depends('borrowed_date', 'state')
    def _compute_days_borrowed(self):
        for record in self:
            if record.state == 'borrowed' and record.borrowed_date:
                record.days_borrowed = (date.today() - record.borrowed_date).days
            else:
                record.days_borrowed = 0

    # 4. Constraint created_date tidak boleh di masa depan
    @api.constrains('created_date')
    def _check_created_date(self):
        for record in self:
            if record.created_date and record.created_date > date.today():
                raise exceptions.ValidationError('Tanggal registrasi tidak boleh di masa depan.')

    # 5. Onchange state kosongkan borrower jika kembali ke available
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'available':
            self.borrower_id = False


    # 7. Cron job: tandai barang borrowed > 30 hari jadi lost
    def _cron_mark_lost_goods(self):
        thirty_days_ago = date.today() - timedelta(days=30)
        overdue_books = self.search([
            ('state', '=', 'borrowed'),
            ('borrowed_date', '<', thirty_days_ago),
        ])
        overdue_books.write({'state': 'lost'})
