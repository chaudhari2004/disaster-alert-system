from flask import Flask, render_template, request, redirect, session
from aws.dynamodb_service import table
from aws.sns_service import send_alert
from aws.s3_service import upload_file
import uuid

app = Flask(__name__)

app.secret_key = 'vivek-secret-key'


# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# ADMIN LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':

            session['admin'] = username

            return redirect('/dashboard')

        else:

            error = 'Invalid Username or Password'

    return render_template(
        'login.html',
        error=error
    )


# SOS FORM
@app.route('/sos', methods=['GET', 'POST'])
def sos():

    if request.method == 'POST':

        request_id = str(uuid.uuid4())

        name = request.form['name']
        location = request.form['location']
        emergency = request.form['emergency']

        image = request.files['image']

        filename = image.filename

        image_url = upload_file(
            image,
            filename
        )

        table.put_item(
            Item={
                'request_id': request_id,
                'name': name,
                'location': location,
                'emergency': emergency,
                'image_url': image_url,
                'status': 'Active'
            }
        )

        alert_message = f"""
🚨 EMERGENCY ALERT 🚨

Citizen Name: {name}

Location: {location}

Emergency Type: {emergency}

Immediate assistance required.
"""

        send_alert(alert_message)

        return render_template(
            'success.html',
            request_id=request_id,
            name=name,
            location=location,
            emergency=emergency,
            image_url=image_url,
            status='Active'
        )

    return render_template('sos.html')


# ADMIN DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'admin' not in session:
        return redirect('/login')

    response = table.scan()

    data = response['Items']

    return render_template(
        'dashboard.html',
        requests=data
    )


# UPDATE STATUS
@app.route('/update-status/<request_id>/<new_status>')
def update_status(request_id, new_status):

    if 'admin' not in session:
        return redirect('/login')

    table.update_item(

        Key={
            'request_id': request_id
        },

        UpdateExpression='SET #s = :val',

        ExpressionAttributeNames={
            '#s': 'status'
        },

        ExpressionAttributeValues={
            ':val': new_status
        }

    )

    return redirect('/dashboard')


# LOGOUT
@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)