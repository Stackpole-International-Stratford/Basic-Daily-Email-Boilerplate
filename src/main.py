import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Load environment variables from example.env
load_dotenv('example.env')

# Database credentials
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME') 

# Email server details
EMAIL_SERVER = os.getenv('EMAIL_SERVER')
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT')
EMAIL_LIST = os.getenv('EMAIL_LIST')

def get_prodmon_ping_entries():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            database=DB_NAME
        )

        cursor = connection.cursor()

        # Retrieve all entries from the table
        query = "SELECT Name, Timestamp FROM prodmon_ping"
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def human_readable_time_diff(past_timestamp):
    now = datetime.utcnow()
    past = datetime.utcfromtimestamp(past_timestamp)
    diff = now - past

    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 604800:
        return f"{int(seconds // 86400)} days"
    elif seconds < 2419200:
        return f"{int(seconds // 604800)} weeks"
    elif seconds < 29030400:
        return f"{int(seconds // 2419200)} months"
    else:
        return f"{int(seconds // 29030400)} years"

def render_template(entries):
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to template.html
        template_path = os.path.join(script_dir, 'template.html')

        with open(template_path, 'r') as file:
            template = file.read()

        # Calculate time since last update for each entry and sort by it
        entries_with_time_diff = []
        for entry in entries:
            epoch_time = entry[1]  # Assuming the timestamp is the second column
            time_diff_seconds = (datetime.utcnow() - datetime.utcfromtimestamp(epoch_time)).total_seconds()

            # Skip entries with a time difference greater than 15 minutes (900 seconds)
            if time_diff_seconds < 900:
                continue

            human_readable_diff = human_readable_time_diff(epoch_time)
            entry_with_time_diff = list(entry) + [human_readable_diff, time_diff_seconds]
            entries_with_time_diff.append(entry_with_time_diff)

        # Sort by time_diff_seconds in ascending order (longest time without update at the top)
        entries_with_time_diff.sort(key=lambda x: x[-1], reverse=True)

        # Generate the HTML table rows
        rows_html = ""
        for entry in entries_with_time_diff:
            human_readable_time = datetime.utcfromtimestamp(entry[1]).strftime('%Y-%m-%d %H:%M:%S')
            row_with_human_readable = entry[:-1] + [human_readable_time]  # Exclude the time_diff_seconds from the output
            rows_html += "<tr>" + "".join(f"<td>{col}</td>" for col in row_with_human_readable) + "</tr>\n"

        rendered_html = template.replace("{{ rows }}", rows_html)

        return rendered_html

    except Exception as e:
        print(f"Failed to read or render template: {e}")
        return None

def send_email(message):
    try:
        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_LIST
        msg['Subject'] = EMAIL_SUBJECT

        msg.attach(MIMEText(message, 'html'))

        # Send the email
        server = smtplib.SMTP(EMAIL_SERVER)
        server.sendmail(EMAIL_FROM, EMAIL_LIST.split(','), msg.as_string())
        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    entries = get_prodmon_ping_entries()
    if entries:
        message = render_template(entries)
        if message:
            send_email(message)
        else:
            print("No relevant entries found or failed to render email template.")
    else:
        print("No entries found or failed to retrieve entries.")

if __name__ == "__main__":
    main()
