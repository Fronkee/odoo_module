import csv
import xmlrpc.client

url = 'http://localhost:8015'
db = 'testing'
username = 'admin'
password = 'admin'

header = ['name', 'age', 'gender']
patients_list = []
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common.version()
# print("version info", common.version())

uid = common.authenticate(db, username, password, {})

if uid:
    print("Authentication Success")
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    patients = models.execute_kw(db, uid, password, 'hospital.patient', 'search_read', [[]],
                                 {'fields': ['name', 'age', 'gender']})

    for val in patients:
        vals = [val['name'], val['age'], val['gender']]
        patients_list.append(vals)
    print(patients_list)

    with open('exported_patients.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(patients_list)
