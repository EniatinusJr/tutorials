{
    'name': 'Estate',
    'version': '0.1',
    'author': 'SnapErp AG',
    'depends': [
        'base',
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}