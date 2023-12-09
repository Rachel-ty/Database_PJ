from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
import requests
import pymysql
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import seaborn as sns
import base64
from io import BytesIO
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = "TYHuang"

db_config = {
    'host': 'localhost',
    'user': 'DB_admin',
    'password': 'DB_admin',
    'db': 'DB_PJ'
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

    
@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


class QueryForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/query', methods=['GET', 'POST'])
# @login_required
def query():
    query_form = QueryForm()
    record = None
    if query_form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(query_form.query.data)
        record = cursor.fetchall()
        
        cursor.close()
        conn.close()
        # return redirect(url_for('index'))  # how to redirect
    return render_template('query.html', form=query_form, record=record)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email=email

    @staticmethod
    @login_manager.user_loader
    def get(user_id):
        # Todo: Write query get user from database
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute('SELECT * FROM Customer Where CustomerId=%s',(user_id,))
        user_data=cur.fetchone()
        cur.close()
        conn.close()
        print(user_data)
        if user_data:
            return User(id=user_data[0],email=user_data[4])
        return None
    


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    billing_address = StringField('Billing Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Todo: Write query to insert user into database; add logic checking
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        insert_query = """
            INSERT INTO Customer (UserName, Email, Password, BillingAddress) 
            VALUES (%s, %s, %s, %s)
        """
        data = (
            form.username.data, 
            form.email.data, 
            form.password.data, 
            form.billing_address.data
        )
        try:
            cursor.execute(insert_query, data)
            conn.commit()  # commit to make changes persistent in the database
            print("Query executed successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # rollback to the previous state if any error occurred
        print(cursor.fetchall())   
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Todo: validate user login info
        email=form.email.data
        password=form.password.data
        print(email,password)
        conn=get_db_connection()
        # cur=conn.cursor()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM Customer WHERE Email=%s', (email,))
        user=cur.fetchone()
        print(user)
        cur.close()
        conn.close()
        if user and user['Password']==password:
            user=User(id=user['CustomerID'],email=user['Email'])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password")

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

class ServiceLocationForm(FlaskForm):
    building=StringField('Building', validators=[DataRequired()])
    unit_number=IntegerField('Unit Number', validators=[DataRequired()])
    takeover_time=DateField('Takeover Time', validators=[DataRequired()])
    square_footage=IntegerField('Square Footage',validators=[DataRequired()])
    number_of_bedrooms= IntegerField('Number of Bedrooms', validators=[DataRequired()])
    number_of_occupants= IntegerField('Number of Occupants', validators=[DataRequired()])
    zcode=StringField('Zip Code',validators=[DataRequired()])
    submit=SubmitField('Add Location')

@app.route('/locations', methods=['GET', 'POST'])
@login_required
def locations():
    # Todo: Write query to get devices from database (done)
    # Todo: Allow user to delete a device (done)
    # Todo: Allow user to add a location by submitting a form (done)
    form=ServiceLocationForm()
    conn=get_db_connection()
    cur=conn.cursor(pymysql.cursors.DictCursor)

    if form.validate_on_submit():
        data=(
            current_user.id,
            form.building.data,
            form.unit_number.data,
            form.takeover_time.data,
            form.square_footage.data,
            form.number_of_bedrooms.data,
            form.number_of_occupants.data,
            form.zcode.data
        )
        cur.execute('INSERT INTO ServiceLocation (CustomerID, Building, UnitNumber, TakeOverDate, SquareFootage, NumberOfBedrooms, NumberOfOccupants, Zcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', data)
        conn.commit()

    cur.execute('Select * from ServiceLocation where CustomerID=%s',(current_user.id,))
    locations=cur.fetchall()
    cur.close()
    conn.close()

   # locations = [{"CustomerID": 1,
   #             "ServiceLocationID": 1,
   #             "Building": "123 Maple St Building", 
   #             "UnitNumber": 5, 
   #             "TakeOverTime": "2021-06-01",
   #             "SquareFootage": 1200,
   #             "NumberOfBedrooms": 2,
   #             "NumberOfOccupants": 4,
   #             "Zcode": '12345'}]
    return render_template('locations.html', form=form, locations=locations)

@app.route('/delete_location/<int:location_id>', methods=['POST'])
@login_required
def delete_location(location_id):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('Delete from Event where DeviceID in (Select DeviceID from Device where ServiceLocationID=%s)', (location_id,))
    cur.execute('DELETE FROM Device WHERE ServiceLocationID = %s', (location_id,))
    cur.execute('DELETE FROM ServiceLocation WHERE ServiceLocationID = %s', (location_id,))
    conn.commit()

    cur.close()
    conn.close()

    flash('Service location deleted successfully')
    return redirect(url_for('locations'))

class NewDeviceForm(FlaskForm):
    first_choice = SelectField('Device Type', 
                               choices=[('AC System', 'AC System'),  # (value, label)
                                        ('Refrigerator', 'Refrigerator')])
    second_choice = SelectField('Device Model', choices=[])
    submit = SubmitField('Add Device')


@app.route('/location/<int:location_id>', methods=['GET', 'POST'])
@login_required
def devices(location_id):
    # Todo: Write query to get all devices from database and show them (done)
    # Todo: Allow user to delete a device (done)
    # Todo: Allow user to add new device by  (DONE)
    #   1. first selecting from user prestored device type list
    #   2. choose the device model from the prestored model list
    form = NewDeviceForm()
    conn=get_db_connection()
    cur=conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':

        device_type = form.first_choice.data
        device_model = form.second_choice.data
        if form.first_choice.data == 'AC System':
            form.second_choice.choices = [('LG AC310', 'LG AC310'), ('Samsung AC123', 'Samsung AC123')]
        elif form.first_choice.data == 'Refrigerator':
            form.second_choice.choices = [('LG Fridge 400', 'LG Fridge 400'), ('Samsung Fridge500', 'Samsung Fridge500')]
    if form.validate_on_submit():
        cur.execute('INSERT INTO Device (ServiceLocationID, Type, ModelName) VALUES (%s, %s, %s)', 
                    (location_id, device_type, device_model))
        conn.commit()
        flash('New device added')
        return redirect(url_for('devices', location_id=location_id))
    cur.execute('Select * from Device where ServiceLocationID=%s',(location_id,))
    devices=cur.fetchall()
    cur.close()
    conn.close()

    return render_template('devices.html', devices=devices, form=form,location_id=location_id)

@app.route('/location/<int:location_id>/delete_device/<int:device_id>', methods=['POST'])
@login_required
def delete_device(location_id,device_id):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    cur.execute('DELETE FROM Device WHERE DeviceID = %s', (device_id,))
    conn.commit()

    cur.close()
    conn.close()

    flash('Device deleted successfully')
    return redirect(url_for('devices', location_id=location_id))


class AnalysisForm(FlaskForm):
    choice = SelectField('Analysis Choice', 
                               choices=[('Energy use', 'Energy use'),  # (value, label)
                                        ('Energy charges', 'Energy charges'),
                                        ('Piechart for energy use percentage per device type', 'Piechart for energy use percentage per device type')])
    submit = SubmitField('Submit')
@app.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    form = AnalysisForm()
    if form.choice.data == 'Energy use':
        return redirect(url_for('energy_use_analysis'))
    elif form.choice.data == 'Energy charges':
        return redirect(url_for('energy_charges_analysis'))
    elif form.choice.data == 'Piechart for energy use percentage per device type':
        return redirect(url_for('piechart'))
    else:
        pass
    return render_template('analysis.html', form=form)
    
    

'''
First View: Energy use analysis
'''
class EnergyUseForm(FlaskForm):
    # 初始化表单时，加载 customer_id 选项
    def __init__(self, *args, **kwargs):
        super(EnergyUseForm, self).__init__(*args, **kwargs)
        self.load_customer_ids()

    def load_customer_ids(self):
        conn = get_db_connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT CustomerID FROM Customer')
        customer_ids = cur.fetchall()
        choices = [('all', 'All')] + [(str(cid['CustomerID']), str(cid['CustomerID'])) for cid in customer_ids]
        self.customer_id.choices = choices
        cur.close()
        conn.close()

    customer_id = SelectField('Customer ID', choices=[('all', 'All')])
    ServiceLocationID = SelectField('Service Location', choices=[('all', 'All')])
    device_type = SelectField('Device Type', choices=[('all', 'All')])
    device_id = SelectField('Device ID', choices=[('all', 'All')])
    Time_granularity = SelectField('Time Granularity', choices=[('daily', 'Daily'), ('monthly', 'Monthly')])
    submit = SubmitField('Submit')
    def update_choices(self, customer_id, service_location_id, device_type):
        # 更新 ServiceLocationID 的选项
        self.ServiceLocationID.choices = get_service_locations(customer_id)
        # 更新 device_type 的选项
        self.device_type.choices = get_device_types(customer_id, service_location_id)
        # 更新 device_id 的选项
        self.device_id.choices = get_device_ids(customer_id, service_location_id, device_type)

@app.route('/get_service_locations/<customer_id>')
@login_required
def get_service_locations(customer_id):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if customer_id == 'all':
        cur.execute('SELECT ServiceLocationID FROM ServiceLocation')
    else:
        cur.execute('SELECT ServiceLocationID FROM ServiceLocation WHERE CustomerID = %s', (customer_id,))
    service_locations = [{'ServiceLocationID': 'all'}] + cur.fetchall()
    cur.close()
    conn.close()
    print(service_locations)
    return [(str(loc['ServiceLocationID']), str(loc['ServiceLocationID'])) for loc in service_locations]

@app.route('/get_device_types/<customer_id>/<service_location_id>')
@login_required
def get_device_types(customer_id, service_location_id):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if service_location_id == 'all':
        if customer_id == 'all':
            cur.execute('SELECT DISTINCT Type FROM Device')
        else:
            cur.execute('SELECT DISTINCT Type FROM Device WHERE ServiceLocationID IN (SELECT ServiceLocationID FROM ServiceLocation WHERE CustomerID = %s)', (customer_id,))
    else:
        cur.execute('SELECT DISTINCT Type FROM Device WHERE ServiceLocationID = %s', (service_location_id,))
    device_types = [{'Type': 'all'}] + cur.fetchall()
    cur.close()
    conn.close()
    return [(str(type['Type']), str(type['Type'])) for type in device_types]

@app.route('/get_device_ids/<customer_id>/<service_location_id>/<device_type>')
@login_required
def get_device_ids(customer_id, service_location_id, device_type):
    conn = get_db_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    query = 'SELECT DeviceID FROM Device WHERE'
    conditions = []
    params = []

    if customer_id != 'all':
        conditions.append('ServiceLocationID IN (SELECT ServiceLocationID FROM ServiceLocation WHERE CustomerID = %s)')
        params.append(customer_id)

    if service_location_id != 'all':
        conditions.append('ServiceLocationID = %s')
        params.append(service_location_id)

    if device_type != 'all':
        conditions.append('Type = %s')
        params.append(device_type)

    if not conditions:
        conditions.append('1')  # Always true condition to fetch all
    where_clause = ' AND '.join(conditions) if conditions else '1'
    sql_query = f'''
                    SELECT DeviceID FROM Device WHERE {where_clause}
                '''
    cur.execute(sql_query, tuple(params))
    device_ids = [{'DeviceID': 'all'}] + cur.fetchall()
    cur.close()
    conn.close()
    print(device_ids)
    return [(str(device['DeviceID']), str(device['DeviceID'])) for device in device_ids]

@app.route('/analysis/energy_use_analysis', methods=['GET', 'POST'])
@login_required
def energy_use_analysis():
    # Todo: provide several(4-5) analysis options(views) for user to choose
    # Todo: create visualization for each analysis option
    form = EnergyUseForm()
    analysis_data=None
    image_base64=None
    if request.method=='POST':
        form.update_choices(form.customer_id.data, form.ServiceLocationID.data, form.device_type.data)
        if form.validate_on_submit():
            conn = get_db_connection()
            cur=conn.cursor(pymysql.cursors.DictCursor)
            plt.figure(figsize=(10, 6))
            conditions = []
            params = []
            if form.customer_id.data != 'all':
                conditions.append('ServiceLocation.CustomerID = %s')
                params.append(form.customer_id.data)
            if form.ServiceLocationID.data != 'all':
                conditions.append('ServiceLocation.ServiceLocationID = %s')
                params.append(form.ServiceLocationID.data)
            if form.device_type.data != 'all':
                conditions.append('Device.Type = %s')
                params.append(form.device_type.data)
            if form.device_id.data != 'all':
                conditions.append('Device.DeviceID = %s')
                params.append(form.device_id.data)

            where_clause = ' AND '.join(conditions) if conditions else '1'

            if form.Time_granularity.data=='daily':
                sql_query = f'''
                    SELECT DATE(Event.Timestamp) AS Date, SUM(Value) AS TotalEnergy
                    FROM Event
                    JOIN Device ON Event.DeviceID = Device.DeviceID
                    JOIN ServiceLocation ON Device.ServiceLocationID = ServiceLocation.ServiceLocationID
                    WHERE EventLabel = 'Energy Use' AND {where_clause}
                    GROUP BY Date(Event.Timestamp)
                '''
                cur.execute(sql_query, tuple(params))
                analysis_data = cur.fetchall()
                df = pd.DataFrame(analysis_data)
                sns.barplot(x="Date", y="TotalEnergy", data=df)
            if form.Time_granularity.data=='monthly':
                sql_query = f'''
                    SELECT MONTH(Event.Timestamp) AS Month, SUM(Value) AS TotalEnergy
                    FROM Event
                    JOIN Device ON Event.DeviceID = Device.DeviceID
                    JOIN ServiceLocation ON Device.ServiceLocationID = ServiceLocation.ServiceLocationID
                    WHERE EventLabel = 'Energy Use' AND {where_clause}
                    GROUP BY YEAR(Event.Timestamp), MONTH(Event.Timestamp)
                '''
                cur.execute(sql_query, tuple(params))
                analysis_data = cur.fetchall()
                df = pd.DataFrame(analysis_data)
                sns.barplot(x="Month", y="TotalEnergy", data=df)
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            image_base64 = base64.b64encode(img.getvalue()).decode()
            cur.close()
            conn.close()
            
    return render_template('energyUse.html', form=form, analysis_data=analysis_data, image_base64=image_base64)

'''
First view ends
'''


'''
Second view: Energy charges analysis
'''
class EnergyChargesForm(FlaskForm):
    # 初始化表单时，加载 customer_id 选项
    def __init__(self, *args, **kwargs):
        super(EnergyChargesForm, self).__init__(*args, **kwargs)
        self.load_customer_ids()

    def load_customer_ids(self):
        conn = get_db_connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT CustomerID FROM Customer')
        customer_ids = cur.fetchall()
        choices = [('all', 'All')] + [(str(cid['CustomerID']), str(cid['CustomerID'])) for cid in customer_ids]
        self.customer_id.choices = choices
        cur.close()
        conn.close()

    customer_id = SelectField('Customer ID', choices=[('all', 'All')])
    ServiceLocationID = SelectField('Service Location', choices=[('all', 'All')])
    device_type = SelectField('Device Type', choices=[('all', 'All')])
    device_id = SelectField('Device ID', choices=[('all', 'All')])
    Time_granularity = SelectField('Time Granularity', choices=[('daily', 'Daily'), ('monthly', 'Monthly')])
    submit = SubmitField('Submit')
    def update_choices(self, customer_id, service_location_id, device_type):
        # 更新 ServiceLocationID 的选项
        self.ServiceLocationID.choices = get_service_locations(customer_id)
        # 更新 device_type 的选项
        self.device_type.choices = get_device_types(customer_id, service_location_id)
        # 更新 device_id 的选项
        self.device_id.choices = get_device_ids(customer_id, service_location_id, device_type)

@app.route('/analysis/energy_charges_analysis', methods=['GET', 'POST'])
@login_required
def energy_charges_analysis():
    # Todo: provide several(4-5) analysis options(views) for user to choose
    # Todo: create visualization for each analysis option
    form = EnergyChargesForm()
    analysis_data=None
    image_base64=None
    if request.method=='POST':
        form.update_choices(form.customer_id.data, form.ServiceLocationID.data, form.device_type.data)
        if form.validate_on_submit():
            conn = get_db_connection()
            cur=conn.cursor(pymysql.cursors.DictCursor)
            plt.figure(figsize=(10, 6))
            conditions = []
            params = []
            if form.customer_id.data != 'all':
                conditions.append('ServiceLocation.CustomerID = %s')
                params.append(form.customer_id.data)
            if form.ServiceLocationID.data != 'all':
                conditions.append('ServiceLocation.ServiceLocationID = %s')
                params.append(form.ServiceLocationID.data)
            if form.device_type.data != 'all':
                conditions.append('Device.Type = %s')
                params.append(form.device_type.data)
            if form.device_id.data != 'all':
                conditions.append('Device.DeviceID = %s')
                params.append(form.device_id.data)

            where_clause = ' AND '.join(conditions) if conditions else '1'

            if form.Time_granularity.data=='daily':
                sql_query = f'''
                    SELECT DATE(Event.Timestamp) AS Date, SUM(Value*Price) AS TotalCharge
                    FROM Event
                    JOIN Device ON Event.DeviceID = Device.DeviceID
                    JOIN ServiceLocation ON Device.ServiceLocationID = ServiceLocation.ServiceLocationID 
                    JOIN EnergyPrice ON ServiceLocation.Zcode=EnergyPrice.Zcode and EXTRACT(HOUR FROM Event.Timestamp) = EXTRACT(HOUR FROM EnergyPrice.Timestamp) and EXTRACT(DAY FROM Event.Timestamp) = EXTRACT(DAY FROM EnergyPrice.Timestamp) and EXTRACT(MONTH FROM Event.Timestamp) = EXTRACT(MONTH FROM EnergyPrice.Timestamp) and EXTRACT(YEAR FROM Event.Timestamp) = EXTRACT(YEAR FROM EnergyPrice.Timestamp)
                    WHERE EventLabel = 'Energy Use' AND {where_clause}
                    GROUP BY Date(Event.Timestamp)
                '''
                cur.execute(sql_query, tuple(params))
                analysis_data = cur.fetchall()
                df = pd.DataFrame(analysis_data)
                sns.barplot(x="Date", y="TotalCharge", data=df)
            if form.Time_granularity.data=='monthly':
                sql_query = f'''
                    SELECT MONTH(Event.Timestamp) AS Month, SUM(Value*Price) AS TotalCharge
                    FROM Event
                    JOIN Device ON Event.DeviceID = Device.DeviceID
                    JOIN ServiceLocation ON Device.ServiceLocationID = ServiceLocation.ServiceLocationID
                    JOIN EnergyPrice ON ServiceLocation.Zcode=EnergyPrice.Zcode and EXTRACT(HOUR FROM Event.Timestamp) = EXTRACT(HOUR FROM EnergyPrice.Timestamp) and EXTRACT(DAY FROM Event.Timestamp) = EXTRACT(DAY FROM EnergyPrice.Timestamp) and EXTRACT(MONTH FROM Event.Timestamp) = EXTRACT(MONTH FROM EnergyPrice.Timestamp) and EXTRACT(YEAR FROM Event.Timestamp) = EXTRACT(YEAR FROM EnergyPrice.Timestamp)
                    WHERE EventLabel = 'Energy Use' AND {where_clause}
                    GROUP BY YEAR(Event.Timestamp), MONTH(Event.Timestamp)
                '''
                cur.execute(sql_query, tuple(params))
                analysis_data = cur.fetchall()
                df = pd.DataFrame(analysis_data)
                sns.barplot(x="Month", y="TotalCharge", data=df)
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            image_base64 = base64.b64encode(img.getvalue()).decode()
            cur.close()
            conn.close()
            
    return render_template('energyCharges.html', form=form, analysis_data=analysis_data, image_base64=image_base64)


'''
Second view ends
'''


'''
Third view: Piechart for energy use percentage per device type
'''

class PiechartForm(FlaskForm):
    serviceLocationID = SelectField('Service Location', choices=[('all', 'All')], validators=[DataRequired()])
    time_granularity = SelectField('Time Granularity', choices=[('daily', 'Daily'), ('monthly', 'Monthly')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/analysis/piechart', methods=['GET', 'POST'])
@login_required
def piechart():
    form = PiechartForm()
    image_base64 = None
    if request.method=='POST':
        conn = get_db_connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        month = str(form.date.data.month)

        if form.time_granularity.data == 'daily':
            pass
        elif form.time_granularity.data == 'monthly':
            cur.execute('SELECT Type, SUM(Value) AS TotalEnergyUse FROM (Event JOIN Device ON Event.DeviceID = Device.DeviceID) JOIN ServiceLocation ON Device.ServiceLocationID = ServiceLocation.ServiceLocationID WHERE EventLabel = "Energy Use" AND CustomerID=1 AND MONTH(TimeStamp) = %s GROUP BY Type', month)
            # Note that service location is not here
        analysis_data = cur.fetchall()
        print(analysis_data)
        
        
        cur.close()
        conn.close()
            
        labels = [data['Type'] for data in analysis_data]
        sizes = [data['TotalEnergyUse'] for data in analysis_data]

        # draw a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

        # save chart to byte stream
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # transfer byte stream to base64 encoded string
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return render_template('piechart.html', form=form, image_base64=image_base64)

'''
Third view ends
'''



if __name__ == '__main__':
    app.run(debug=True, port=8000)