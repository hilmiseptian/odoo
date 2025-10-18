{
    'name': 'Library Module',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'views/library_menus.xml',
        'views/library_partner_views.xml',
        'views/library_book_views.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
}
