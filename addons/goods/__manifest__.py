{
    'name': 'Goods Module',
    'version': '1.0',
    'depends': ['base', 'web'],
    'data': [
        'views/goods_menus.xml',
        'views/borower_views.xml',
        'views/goods_views.xml',
        "report/goods_report.xml",
        "report/goods_report_template.xml",
        'security/ir.model.access.csv',
    ],
    'application': True,
}
