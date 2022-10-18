{
    'name': 'Hospital Management',
    'version': '1.1.0',
    'license': 'LGPL-3',
    'website': 'www.test.com.mm',
    'category': 'Hospital',
    'author': 'odoo dev',
    'summary': 'Hospital Management System',
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': -100,
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient_view.xml',
    ],
}
