from flask import Flask, render_template_string, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize SQLite database
def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_sqlite_db()


html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disco-Themed Sign In</title>
</head>
<body style="font-family: 'Arial', sans-serif; background-color: black; color: white; text-align: center; margin: 0; padding: 0; height: 100vh; display: flex; justify-content: center; align-items: center; overflow: hidden;">
    <div style="background: linear-gradient(45deg, #ff0066, #ffcc00, #66ff66, #00ccff); background-size: 400% 400%; animation: disco 5s infinite; padding: 30px; border-radius: 15px; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);">
        <div style="width: 100px; height: 100px; background: radial-gradient(circle, #ffffff, #cccccc); border-radius: 50%; margin: 0 auto 30px; box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); animation: spin 3s infinite linear;"></div>
        <h1 style="font-size: 3rem; margin-bottom: 20px;">Sign In</h1>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul style="color: red;">
              {% for message in messages %}
                <li>{{ message }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        <form method="POST" action="{{ url_for('login') }}">
            <label for="email" style="display: block; margin: 10px 0 5px;">Email:</label>
            <input type="email" id="email" name="email" required style="width: 80%; padding: 10px; margin-bottom: 15px; border: none; border-radius: 5px; box-shadow: 0 0 10px rgba(255, 255, 255, 0.5); font-size: 1.2rem;">
            
            <label for="password" style="display: block; margin: 10px 0 5px;">Password:</label>
            <input type="password" id="password" name="password" required style="width: 80%; padding: 10px; margin-bottom: 15px; border: none; border-radius: 5px; box-shadow: 0 0 10px rgba(255, 255, 255, 0.5); font-size: 1.2rem;">
            
            <div class="remember-me" style="margin: 20px 0;">
                <input type="checkbox" id="remember-me" name="remember-me">
                <label for="remember-me">Remember Me</label>
            </div>
            
            <button type="submit" style="background-color: #ff0066; border: none; padding: 15px 30px; border-radius: 30px; box-shadow: 0 0 10px rgba(255, 255, 255, 0.5); font-size: 1.2rem; cursor: pointer; transition: all 0.3s ease;">Sign In</button>
        </form>
    </div>

    <script>
        // Add keyframes for disco animation
        const styleSheet = document.createElement("style");
        styleSheet.type = "text/css";
        styleSheet.innerText = `
            @keyframes disco {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(styleSheet);
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            stored_password = user[2]
            if check_password_hash(stored_password, password):
                flash("Login successful!", "success")
                return redirect(url_for('login'))
            else:
                flash("Incorrect password!", "error")
        else:
            flash("User not found!", "error")
        
        conn.close()

    return render_template_string(html_template)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            flash("Registration successful!", "success")
        except sqlite3.IntegrityError:
            flash("Email already exists!", "error")

        conn.close()
        return redirect(url_for('login'))

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
