from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'DB_admin',
    'password': 'DB_admin',
    'db': 'DB_PJ'
}


def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

    
@app.route('/', methods=['GET'])
def main_page():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("""
        SELECT Device.DeviceId, SUM(Event.Value) AS TotalConsumption 
        FROM Event 
        JOIN Device ON Event.DeviceId = Device.DeviceId 
        WHERE EventLabel = 'Energy Use' 
        AND Timestamp > '2023-08-01 15:40:00' - INTERVAL 1 DAY 
        AND Device.ServiceLocationId IN (
            SELECT ServiceLocationId 
            FROM ServiceLocation 
            WHERE CustomerId = 1
        ) 
        GROUP BY Device.DeviceId;
    """)
    
    record = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(record)

if __name__ == '__main__':
    app.run()