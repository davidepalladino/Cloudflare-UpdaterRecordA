import os
import sys

from logging.handlers import TimedRotatingFileHandler
from requests import get

from facades.environment import Environment
from facades.cloudflare import Cloudflare
from utils.logger import *
from utils.messages import ERROR_NO_RECORD_NAME, ERROR_RECORD_NOT_FOUND, ERROR_RECORD_UPDATE_FAILED, INFO_IP_CHANGED, \
    INFO_RECORD_UPDATED

ARG_NAME: str = "-name"

def main():
    """
    Main function to update a Cloudflare DNS record with the current public IP address.

    This script automates the process of:
    1. Fetching the current public IP address from https://api.ipify.org.
    2. Validating and retrieving the specified DNS record via the Cloudflare API.
    3. Updating the DNS record if the public IP address has changed.

    Usage:
        python main.py -name <record_name>

    Requirements:
        - Command-line argument `-name <record_name>` is required.
        - Environment variables `ZONE_ID`, `EMAIL`, and `API_KEY` must be set (preferably using a `.env` file).
        - The following Python modules must be installed:
            - `requests` for making HTTP requests.
            - `python-dotenv` for loading environment variables.

    Steps:
        1. Validate that the `-name <record_name>` argument is provided.
        2. Set up logging with a daily rotating log file stored in the `logs` directory.
        3. Fetch the public IP address.
        4. Initialize the Cloudflare API wrapper using credentials from environment variables.
        5. Retrieve the specified DNS record by name.
        6. Compare the DNS record's content with the public IP address.
        7. Update the DNS record if the IP has changed and log the results.

    Error Handling:
        - Logs and exits if the `-name` argument or the DNS record is missing.
        - Logs errors if required environment variables are not set or if the update process fails.

    Logs:
        - Log files are stored in the `logs` directory and rotated daily.
        - Logs include information about IP changes, successful updates, and error details.

    """
    exec_path = sys.argv[0].removesuffix("/main.py")

    log_path = "{0}/logs".format(exec_path)
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    args = sys.argv[1:]
    if len(args) < 2 or args[0] != ARG_NAME:
        record_name = None
    else:
        record_name = args[1]

    logging.basicConfig(
        format="[%(asctime)s] {0} - %(levelname)s: %(message)s".format(record_name),
        level=logging.INFO,
        handlers=[
            TimedRotatingFileHandler(
                filename="{0}/logs/main".format(exec_path),
                when="midnight",
                interval=1,
                backupCount=15
            )
        ]
    )

    if record_name is None:
        log(ERROR_NO_RECORD_NAME, LogGravity.ERROR)
        exit(1)

    try:
        environment = Environment()
    except EnvironmentError as error:
        log(error, LogGravity.ERROR)
        exit(1)

    public_ip = get('https://api.ipify.org').content.decode('utf8')
    cloudflare = Cloudflare(
        zone_id=environment.get_zone_id(),
        email=environment.get_email(),
        api_key=environment.get_api_key()
    )

    record = cloudflare.get_record(record_name)
    if record is None:
        log(ERROR_RECORD_NOT_FOUND, LogGravity.ERROR)
        exit(1)

    if record['content'] != public_ip:
        log(INFO_IP_CHANGED.format(record['content'], public_ip), LogGravity.INFO)
        errors: list[str] = cloudflare.update_record(record['id'], public_ip)
        if len(errors) == 0:
            log(INFO_RECORD_UPDATED, LogGravity.INFO)
        else:
            log(ERROR_RECORD_UPDATE_FAILED.format(errors), LogGravity.ERROR)

if __name__ == '__main__':
    main()