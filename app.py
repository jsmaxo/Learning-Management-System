from flask import Flask, render_template, url_for, request, flash, redirect
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

# --- Database Config ---
DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "admin"

# --- Database Connection ---
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST
    )
    print("✅ Database connected successfully")
except Exception as e:
    print("❌ Unable to connect to database:", e)


# --- Routes ---
@app.route('/')
def index():
    return render_template('sign_up.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        nic = request.form['nic']
        mobile = request.form['mobile']
        address1 = request.form['address1']
        address2 = request.form['address2']
        district = request.form['district']

        cur.execute(
            "INSERT INTO students (first_name, last_name, nic, mobile, address1 ,address2 ,district) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (fname, lname, nic, mobile, address1, address2, district)
        )
        conn.commit()
        print(f"✅ Student added successfully: {fname} {lname}, NIC: {nic}")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True , port=5000)
