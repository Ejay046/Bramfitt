from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
import requests

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ejay046:Password101!@localhost/technical_test_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Record(db.Model):

    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    requested_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    request_info = db.Column(JSON)

    def __repr__(self, requested_time, request_info):
        self.request_info = request_info
        self.requested_time = requested_time


url = 'https://api.tfl.gov.uk/StopPoint/490009333W/arrivals'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        current_time = datetime.utcnow()
        response = requests.get(url)
        info = response.json()
        new_record = Record(request_info=info, requested_time=current_time)
        try:
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('details', id=new_record.id))
        except:
            return 'There was an issue storing your request'
    else:
        return render_template('index.html')


@app.route('/history', methods=['GET'])
def get_history():
    records = Record.query.order_by(Record.requested_time).all()
    return render_template('history.html', records=records)


@app.route('/details/<int:id>')
def details(id):
    record = Record.query.get_or_404(id)
    return render_template('details.html', record=record, length=len(record.request_info), information=record.request_info)


@app.route('/details/<int:id>/json')
def view_json(id):
    record = Record.query.get_or_404(id)
    return render_template('json.html', record=record)


if __name__ == "__main__":
    app.run(debug=True)
