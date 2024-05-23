from datetime import datetime, timedelta
from utils.logging_utils import setup_logger
import jinja2
import traceback
import os
import sys

logger = setup_logger()

def shift_times(date, date_offset=0):
    # """
    # Shifts the given date by a specified number of days and returns the start and end dates.

    # Parameters:
    # - date: The base date for shifting.
    # - date_offset (optional): The number of days to offset the date. Defaults to 0.

    # Returns:
    # - start_date: The start date after shifting.
    # - end_date: The end date after shifting.
    # """

    # end_date is this morning at 7am
    end_date = date.replace(hour=7, minute=0, second=0, microsecond=0)
    # adjust end_date by date_offset days
    end_date = end_date - timedelta(days=date_offset)
    # start_date is yesterday morning at 7am
    start_date = end_date - timedelta(hours=24)
    end_date = end_date - timedelta(seconds=1)
    return start_date, end_date




def render_report(data, start, end, report_title):
    """
    Render a report HTML using Jinja2 templates based on the provided data, start time, end time, and report title.
    The function loads a template from the 'templates' directory, injects the data and additional variables into the template,
    and returns the rendered HTML content.

    Parameters:
    data (list of dict): The data to be included in the report, typically containing information about parts.
    start (datetime): The start time for the report period.
    end (datetime): The end time for the report period.
    report_title (str): The title of the report, which can be dynamically set.

    Returns:
    str: The rendered HTML content of the report.

    Raises:
    jinja2.TemplateError: If there is an error during template rendering.
    """
    try:
        # Get the directory path where main.py is located
        current_directory = os.path.dirname(__file__)
        
        # Construct the path to the templates directory
        template_path = os.path.join(current_directory, '..', 'templates')

        # Load the template from the templates directory
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
        template = env.get_template('template.html')

        # Format start and end times for display
        formatted_start_time = start.strftime("%Y-%m-%d %I:%M %p")
        formatted_end_time = end.strftime("%Y-%m-%d %I:%M %p")

        # Render the template with the provided data and additional variables
        return template.render(data=data, report_title=report_title, report_period=f"{formatted_start_time} to {formatted_end_time}")
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        traceback.print_exc()
        raise
