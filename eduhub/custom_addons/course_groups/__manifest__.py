{
    'name': 'EduHUB CRM',
    'version': '1.0',
    'website': 'https://www.bahromnajmiddinov.com',
    'author': 'Bahrom Najmiddinov',
    'description': """
         EduHUB management system.
    """,
    'category': '',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/invoice_groups.xml',
        'security/ir.model.access.csv',

        'views/menu_items.xml',

        'data/eduhub.week.day.csv',
        'data/eduhub_invoicing_sequence.xml',

        'views/courses.xml',
        'views/groups.xml',
        'views/invoice.xml',
        'views/salary.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}