#app.py
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import sqlite3, os
from payment import payment_bp
from generate_pdf import generate_pdf
import sys

app = Flask(__name__)
app.register_blueprint(payment_bp)

if not os.path.exists('static/receipts'):
    os.makedirs('static/receipts')


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/thankyou/<int:donation_id>')
def thankyou(donation_id):
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('SELECT verified FROM donations WHERE id = ?', (donation_id,))
    verified = c.fetchone()
    conn.close()

    if verified and verified[0] == 1:
        receipt_filename = f"receipt_{donation_id}.pdf"
        receipt_path = os.path.join("static/receipts", receipt_filename)

        if not os.path.exists(receipt_path):
            conn = sqlite3.connect('donations.db')
            c = conn.cursor()
            c.execute('SELECT name, email, amount, donation_type, address FROM donations WHERE id = ?', (donation_id,))
            row = c.fetchone()
            conn.close()
            if row:
                generate_pdf(receipt_path, donation_id, *row)

        return render_template('thankyou.html', receipt_filename=receipt_filename)

    else:
        return "⚠️ Payment not verified yet. Please wait."


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('static/receipts', filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)




# Fix path issues for PyInstaller
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
template_folder = os.path.join(base_path, 'templates')
static_folder = os.path.join(base_path, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
