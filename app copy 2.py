from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)

# MySQL database configuration

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'dsr',
}

# Create a connection to the MySQL database
db = mysql.connector.connect(**db_config)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.ipage.com'  # Set your SMTP server
app.config['MAIL_PORT'] = 587  # Set your SMTP server port
app.config['MAIL_USERNAME'] = 'menaga.veeramani@winvinayafoundation.org'  # Set your SMTP username
app.config['MAIL_PASSWORD'] = 'Wvf@2468)'  # Set your SMTP password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'menaga.veeramani@winvinayafoundation.org'  # Set your default "From" email address

mail = Mail(app)

# Mapping of names to email addresses
name_to_email = {
    "Menaga": "menaga.veeramani@winvinayafoundation.org",
    "Dharanidaran": "saravana.p@winvinayafoundation.org",
    # Add more names and email addresses as needed
}
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    # Implement your authentication logic here
    if username == 'admin' and password == 'winvinaya':
        return redirect(url_for('submit_index_form'))
    elif(username == 'Winvinaya' and password == 'Grow@wvf123&'):
        return redirect(url_for('submit_index_form'))
    else:
        return redirect(url_for('login'))
    
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        project = request.form.getlist('project[]')
        name = request.form.getlist('Name[]')
        activity = request.form.getlist('Activity[]')
        description = request.form.getlist('Description[]')
        date = request.form.getlist('date[]')  # Update date field
        start_time = request.form.getlist('startTime[]')
        end_time = request.form.getlist('endTime[]')
        effort = request.form.getlist('effort[]')
        total_hours = request.form.get('totalHours')

        print("Project:", project)
        print("Name:", name)
        print("Activity:", activity)
        print("Description:", description)
        print("Date:", date)
        print("Start Time:", start_time)
        print("End Time:", end_time)
        print("Effort:", effort)

        # Find the number of entries (entries count)
        entries_count = len(project)

        cursor = db.cursor()

        for i in range(entries_count):
            # Insert data into the MySQL database
            query = "INSERT INTO status_report (project, name, activity, description, date, start_time, end_time, effort) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (project[i], name[i], activity[i], description[i], date[i], start_time[i], end_time[i], effort[i])
            cursor.execute(query, values)

        db.commit()
        cursor.close()

        # Get the selected name from the form data
        selected_name = name[0]  # Assuming the name is the same for all entries, change as needed
        
        # Use the selected name to dynamically set the "From" email address
        if selected_name in name_to_email:
            from_email = name_to_email[selected_name]
        else:
            # Handle the case where the selected name is not in the mapping
            from_email = app.config['MAIL_DEFAULT_SENDER']  # Set the default email address

        # Send an email after data is inserted into the database
        msg = Message("Daily Status Report", recipients=["darandharani6255@gmail.com"])
        msg.sender = from_email  # Set the "From" email address
        msg.html = f"Hello, {selected_name}<br><br>" \
        f"Project: {', '.join(project)}<br>" \
        f"Activity: {', '.join(activity)}<br>" \
        f"Description: {', '.join(description)}<br>" \
        f"Date: {', '.join(date)}<br>" \
        f"Start Time: {', '.join(start_time)}<br>" \
        f"End Time: {', '.join(end_time)}<br>" \
        f"Effort: {', '.join(effort)} hours<br>" \
        f"Total Working Hours: {total_hours} hours<br><br>" \
        "Thank you for your submission."

        with app.app_context():
            mail.send(msg)

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
