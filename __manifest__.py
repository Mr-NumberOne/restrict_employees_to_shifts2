# -*- coding: utf-8 -*-
{
    'name': 'Employee Shift Restriction',
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Restrict Employee login to there shifts""",
    'description': """Any Employee who is restricted to their shifts, by there administrators, while only have access to the system during there shifts """,
    'license': 'AGPL-3',
    'depends': ['base','hr'],
    'data': [
        'views/hr_employee.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/restrict_employees_to_shifts/static/src/xml/systray.xml',
            '/restrict_employees_to_shifts/static/src/js/systray.js',
            '/restrict_employees_to_shifts/static/src/css/systray.css'
        ],
    },
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
