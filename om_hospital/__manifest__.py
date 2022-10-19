{
    'name': 'Hospital Management',
    'version': '1.1.0',
    'license': 'LGPL-3',
    'website': 'www.test.com.mm',
    'category': 'Hospital',
    'author': 'odoo dev',
    'summary': 'Hospital Management System',
    'auto_install': False,
    'application': True,
    'sequence': -100,
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
    ],
}
