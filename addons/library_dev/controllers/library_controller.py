from odoo import http
from odoo.http import request, Response
import json

class LibraryController(http.Controller):

    @http.route('/api/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books_http(self, **kwargs):
        state_filter = kwargs.get('state')
        domain = []
        if state_filter:
            domain.append(('state', '=', state_filter))

        books = request.env['library.book'].sudo().search(domain)
        result = [{
            'name': book.name,
            'author': book.author,
            'state': book.state,
        } for book in books]

        return Response(
            json.dumps(result),
            content_type='application/json;charset=utf-8'
        )
