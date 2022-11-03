import xmlrpc.client

url = 'http://localhost:8015'
db = 'testing'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common.version()
# print("version info", common.version())

uid = common.authenticate(db, username, password, {})

if uid:
    print("Authentication Success")
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    # search method
    # partner = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])

    # read method
    # partner_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partner], {'fields': ['id', 'name']})
    # print("------->", partner_rec)

    # search read
    # partner_rec2 = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[]], {'fields': ['id', 'name']})
    # print("Search Read ------", partner_rec2)
    #
    # vals = {
    #     'name': 'odoo mates external api',
    #     'email': 'odoomates@gmail.com'
    # }
    # created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
    # print("Create Record ------>", created_id)

    # update data
    # models.execute_kw(db, uid, password, 'res.partner', 'write', [[162], {'mobile': "7777", "phone": "5555"}])

    # unlink data
    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[162]])
