# main.py

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jinja2
from utils.email_utils import send_email, load_email_config
from utils.report_utils import shift_times, render_report
from utils.logging_utils import setup_logger
from data.db import connect_to_database
import traceback

# relative path to the .env file from the current script location
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'example.env')
load_dotenv(dotenv_path=dotenv_path)
logger = setup_logger()


def get_data(conn, start, end):
    # Example function to retrieve data from the database
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT part_number, good, reject_type, reject_count
            FROM parts_table
            WHERE timestamp BETWEEN %s AND %s
        """
        cursor.execute(query, (start, end))
        data = cursor.fetchall()
        return data
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return []


def main():
    # Load email configuration
    email_config = load_email_config()

    # Extract shift_times offset from command line arguments if provided, default to 0
    offset = 0 if len(sys.argv) == 1 else int(sys.argv[1])

    # Calculate start and end times based on current time and offset
    start_time, end_time = shift_times(datetime.now(), offset)

    db_connection = None  # Initialize db_connection variable

    try:
        # Establish database connection
        db_connection = connect_to_database()
        if not db_connection:
            raise Exception("Failed to connect to the database")

        # Retrieve data
        data = get_data(db_connection, start_time, end_time)

        report_title = "AB1V Autogauge"  # Example title, can be dynamically set

        # Render report HTML using retrieved data
        report_html = render_report(data, start_time, end_time, report_title)

        # Send email with the generated report HTML
        send_email(report_html, email_config)

        # Log successful completion of report processing and email sending
        logger.info("Report processing and email sending completed successfully.")

    except Exception as e:
        # Handle any exceptions that occur during the main process and log them
        logger.error(f"An error occurred in the main process: {e}")

    finally:
        if db_connection:
            db_connection.close()


if __name__ == '__main__':
    main()
