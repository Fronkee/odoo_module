{
    'name': 'My Website Theme',
    'description': 'A description for your theme.',
    'version': '1.0',
    'author': 'Your name',
    'data': [
        'views/page.xml',
        'views/assets.xml'
    ],
    'category': 'Theme/Creative',
    'depends': ['website', ],
    'assets': {
        'website.assets_frontend': [
            'theme_tutorial/static/scss/style.scss',
        ]
    }
}
