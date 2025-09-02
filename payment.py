from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3, os, qrcode

payment_bp = Blueprint('payment', __name__)

if not os.path.exists('static/qrcodes'):
    os.makedirs('static/qrcodes')


@payment_bp.route('/donate', methods=['POST'])
def donate():
    name = request.form['name']
    email = request.form['email']
    amount = request.form['amount']
    donation_type = request.form['donation_type']
    address = request.form['address']

    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, amount TEXT, donation_type TEXT, address TEXT, verified INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        INSERT INTO donations (name, email, amount, donation_type, address) 
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, amount, donation_type, address))
    conn.commit()
    donation_id = c.lastrowid
    conn.close()

    # Generate QR code
    qr_data = f"upi://pay?pa=9820672770@okbizaxis&pn={name}&am={amount}&cu=INR"
    qr_path = f"static/qrcodes/qr_{donation_id}.png"
    qr = qrcode.make(qr_data)
    qr.save(qr_path)

    return render_template('show_qr.html', donation_id=donation_id, qr_filename=f"qr_{donation_id}.png", amount=amount)


@payment_bp.route('/verify/<int:donation_id>')
def verify(donation_id):
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('UPDATE donations SET verified = 1 WHERE id = ?', (donation_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('thankyou', donation_id=donation_id))
