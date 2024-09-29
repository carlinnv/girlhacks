from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory user storage (for demonstration purposes)
users = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('index.html', error=True)
    
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('new_username')
    password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('Passwords do not match', 'danger')
        return render_template('index.html', error=True)
    
    if username in users:
        flash('Username already exists', 'danger')
        return render_template('index.html', error=True)

    # Register the user
    users[username] = password
    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
