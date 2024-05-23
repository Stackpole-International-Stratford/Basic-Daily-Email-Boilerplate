# main script

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jinja2
from utils.email_utils import send_email, load_email_config
from utils.report_utils import shift_times, render_report
from utils.logging_utils import setup_logger
import traceback
import _mysql_connector

# relative path to the .env file from the current script location
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'example.env')
load_dotenv(dotenv_path=dotenv_path)
logger = setup_logger()


def get_data(start, end):
#   """
#     Retrieve data for report generation within the specified time range. This is where you would query the database for data, by replacing the dummy data with
#     an actual function to do so.
    
#     Parameters:
#     start (datetime): The start time for data retrieval.
#     end (datetime): The end time for data retrieval.
    
#      Returns:
#       - list: A list of dictionaries, each containing information about parts.
#         Each dictionary could have the following keys for example:
#         - 'part_number': The part number.
#         - 'good': The count of good parts.
#         - 'reject': A dictionary containing information about rejected parts.
#             Each key in the 'reject' dictionary corresponds to a type of rejection,
#             and its value is a dictionary containing the label and count of rejections.
#     Example:
#     [
#         {'part_number': '1234', 'good': 100, 'reject': {'spotface': {'label': 'Spot Face', 'count': 5}}},
#         {'part_number': '5678', 'good': 200, 'reject': {'media': {'label': 'Media', 'count': 3}}},
#         ...
#     ]
#     """   

    # Dummy data
    data = [
        {'part_number': '1234', 'good': 100, 'reject': {'spotface': {'label': 'Spot Face', 'count': 5}}},
        {'part_number': '5678', 'good': 200, 'reject': {'media': {'label': 'Media', 'count': 3}}},
        {'part_number': '2323', 'good': 300, 'reject': {}},
        {'part_number': '1234', 'good': 100, 'reject': {'spotface': {'label': 'Spot Face', 'count': 5}}},
        {'part_number': '5678', 'good': 200, 'reject': {'media': {'label': 'Media', 'count': 3}}},
        {'part_number': '2323', 'good': 300, 'reject': {}},
        {'part_number': '1234', 'good': 100, 'reject': {'spotface': {'label': 'Spot Face', 'count': 5}}},
        {'part_number': '5678', 'good': 200, 'reject': {}},
        {'part_number': '2323', 'good': 300, 'reject': {}},
        {'part_number': '1234', 'good': 100, 'reject': {'spotface': {'label': 'Spot Face', 'count': 5}}},
        {'part_number': '7889', 'good': 150, 'reject': {'burrs': {'label': 'Burrs', 'count': 2}}},
        {'part_number': '9988', 'good': 250, 'reject': {'warp': {'label': 'Warp', 'count': 1}}},
        {'part_number': '5467', 'good': 350, 'reject': {'crack': {'label': 'Crack', 'count': 4}}},
        {'part_number': '2143', 'good': 120, 'reject': {'spotface': {'label': 'Spot Face', 'count': 3}}},
        {'part_number': '8765', 'good': 220, 'reject': {'media': {'label': 'Media', 'count': 6}}},
        {'part_number': '3434', 'good': 330, 'reject': {'porosity': {'label': 'Porosity', 'count': 7}}},
        {'part_number': '1212', 'good': 140, 'reject': {'spotface': {'label': 'Spot Face', 'count': 8}}},
        {'part_number': '4545', 'good': 230, 'reject': {'deformation': {'label': 'Deformation', 'count': 5}}},
        {'part_number': '6767', 'good': 340, 'reject': {'paint': {'label': 'Paint Defect', 'count': 2}}},
        {'part_number': '8989', 'good': 160, 'reject': {'spotface': {'label': 'Spot Face', 'count': 1}}},
        {'part_number': '1010', 'good': 210, 'reject': {'media': {'label': 'Media', 'count': 3}}},
        {'part_number': '3232', 'good': 310, 'reject': {}},
        {'part_number': '5432', 'good': 190, 'reject': {'spotface': {'label': 'Spot Face', 'count': 6}}},
        {'part_number': '7865', 'good': 205, 'reject': {'crack': {'label': 'Crack', 'count': 2}}},
        {'part_number': '3498', 'good': 305, 'reject': {'media': {'label': 'Media', 'count': 5}}},
        {'part_number': '2124', 'good': 115, 'reject': {'spotface': {'label': 'Spot Face', 'count': 3}}},
        {'part_number': '5656', 'good': 225, 'reject': {'deformation': {'label': 'Deformation', 'count': 4}}},
        {'part_number': '7373', 'good': 335, 'reject': {'paint': {'label': 'Paint Defect', 'count': 1}}},
        {'part_number': '9191', 'good': 155, 'reject': {'spotface': {'label': 'Spot Face', 'count': 2}}},
    ]
    return data




def main():
    #   """
    # Main function for orchestrating the generation of a report, rendering it as HTML, and sending it via email.
    # The function retrieves data within a specified time range, renders a report using the retrieved data,
    # and sends the report as an email using SMTP configuration. Any errors that occur during the process are logged.

    # Load email configuraiton from email_utils module
    email_config = load_email_config()

    # Extract the shift_times offset from command line arguments if provided, if there's no command line args then default to 0
    offset = 0 if len(sys.argv) == 1 else int(sys.argv[1])

    # Calculating start and end times based on current time and offset
    start_time, end_time = shift_times(datetime.now(), offset)

    # Format start and end times for display in email
    formatted_start_time = start_time.strftime("%Y-%m-%d %I:%M %p")
    formatted_end_time = end_time.strftime("%Y-%m-%d %I:%M %p")

    try:
        # Retrieving data based on formatted start and end times
        data = get_data(formatted_start_time, formatted_end_time)
        
        report_title = "AB1V Autogauge"  # Example title, can be dynamically set

        # Rendering report HTML using retrieved data
        report_html = render_report(data, start_time, end_time, report_title)
        
        # Sending email with the generated report HTML and email configuration
        send_email(report_html, email_config)
        
        # Logging successful completion of report processing and email sending
        logger.info("Report processing and email sending completed successfully.")
        
    except Exception as e:
        # Handling any exceptions that occur during the main process and logging them
        logger.error(f"An error occurred in the main process: {e}")


if __name__ == '__main__':
    main()
