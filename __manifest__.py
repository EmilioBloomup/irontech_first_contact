{
    'name': "irontech_first_contact",
    'depends': ['base', 'insurance_app', 'mail', 'contacts', 'bloomup_aruba_sms_integration'],
    'application': False,
    'description': """
        Aggiunge cron per ricordare ad una risorsa di effettuare il primo contatto con un cliente 
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/base_config_settings_view.xml',
        'data/cron.xml'
    ]
}