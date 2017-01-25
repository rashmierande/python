from flask import Flask , jsonify, abort, make_response, request
from flask import url_for
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
app = Flask(__name__)

emps = [
    {
        'Id': 1,
        'Name': u'Rashmi',
        'Dept': u'Cloud Eng',
        'Designation': 'Staff Eng'
    },
{
        'Id': 2,
        'Name': u'John',
        'Dept': u'Cloud Eng',
        'Designation': 'Sr.Staff Eng'
    }

]
@auth.get_password
def get_password(username):
    if username == 'rashmi':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def make_public_emp(emp):
    new_emp = {}
    for field in emp:
        if field == 'Id':
            new_emp['uri'] = url_for('get_emps', emp_id=emp['Id'], _external=True)
        else:
            new_emp[field] = emp[field]
    return new_emp

@app.route('/api/emplist', methods=['GET'])
@auth.login_required
def get_emps():
    #return jsonify({'employees': emps})
    return jsonify({'employees': [make_public_emp(emp) for emp in emps]})

@app.route('/api/emps/<int:emp_id>', methods=['GET'])
@auth.login_required
def get_emp(emp_id):
    emp = [emp for emp in emps if emp['Id'] == emp_id]
    if len(emp) == 0:
        abort(404)
    return jsonify({'employee': emp[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/emp/add', methods=['POST'])
@auth.login_required
def create_emp():
    if not request.json or not 'Name' in request.json:
        abort(400)
    emp = {
        'Id': emps[-1]['Id'] + 1,
        'Name': request.json['Name'],
        'Dept': request.json.get('Dept', ""),
        'Designation': request.json.get('Designation',"")
    }
    emps.append(emp)
    return jsonify({'employee': emp}), 201

@app.route('/api/emps/<int:emp_id>', methods=['PUT'])
@auth.login_required
def update_emp(emp_id):
    emp = [emp for emp in emps if emp['Id'] == emp_id]
    if len(emp) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Id' in request.json : #and type(request.json['Id']) != unicode
        abort(400)
    if 'Name' in request.json : #and type(request.json['Name']) is not unicode
        abort(400)

    emp[0]['Designation'] = request.json.get('Designation', emp[0]['Designation'])
    emp[0]['Dept'] = request.json.get('Dept', emp[0]['Dept'])
    return jsonify({'emp': emp[0]})

@app.route('/api/emps/<int:emp_id>', methods=['DELETE'])
@auth.login_required
def delete_task(emp_id):
    emp = [emp for emp in emps if emp['Id'] == emp_id]
    if len(emp) == 0:
        abort(404)
    emps.remove(emp[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)