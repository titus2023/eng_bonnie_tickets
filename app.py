from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buy', methods=['POST'])
def buy_ticket():
    buyer_name = request.form.get('buyer_name')
    new_ticket = Ticket(buyer_name=buyer_name)
    db.session.add(new_ticket)
    db.session.commit()
    return redirect(url_for('confirmation', ticket_id=new_ticket.id))

@app.route('/confirmation/<int:ticket_id>')
def confirmation(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('confirmation.html', ticket=ticket)

@app.route('/tickets')
def ticket_history():
    tickets = Ticket.query.all()
    return render_template('tickets.html', tickets=tickets)

if __name__ == "__main__":
    app.run(debug=True)
