# WARNING: This project has been dismissed. Consider the new project [DSN-UpdaterA](https://github.com/davidepalladino/DNS-UpdaterA)!
___
# Cloudflare DNS Updater
This script manages Cloudflare DNS records by automatically updating them when the public IP changes. 
It interacts with the Cloudflare API to fetch and update DNS records for a specific zone and record name.

## Features
- Fetches the current public IP address.
- Compares the public IP with the content of a specified DNS record.
- Updates the DNS record if the IP has changed.
- Provides detailed logging for debugging and monitoring purposes.

## Requirements
- Python 3.7 or higher.
- The following Python modules:
    - `requests`
    - `python-dotenv`
    - `logging`

## Installation 
1. Clone or download this repository to your local machine.
2. Install the required Python dependencies using `pip`:
```bash
pip install requests python-dotenv
```
or
```bash
pip install -r requirements.txt 
```
3. Create a `.env` file in the script directory with the required environment variables as described in the Configuration section.

### Configuration
The script relies on environment variables for configuration. Create a `.env` file in the script's directory with the following variables:

```env
ZONE_ID=your_zone_id
EMAIL=your_cloudflare_email
API_KEY=your_cloudflare_api_key
```
- `ZONE_ID`: Your Cloudflare Zone ID for the domain.
- `EMAIL`: The email associated with your Cloudflare account.
- `API_KEY`: Your Cloudflare API key.

## Usage
Run the script directly from the terminal with the record name as an argument:
```bash
python main.py -name <record_name>
```

## Expected Output
1. If the DNS record is not found:
```
ERROR: Record not found.
```

2. If the IP address has changed:
```
INFO: IP is changed. Was <old_ip>, now is <new_ip>.
INFO: Record updated.
```
3. If the IP address remains the same:
```
INFO: IP is same.
```
4. If the record update fails:
```
ERROR: Record update failed with these reasons: [...]
```

## Notes
- The script modifies only the content field of the DNS record.
- Ensure your Cloudflare API key has sufficient permissions to read and update DNS records.
- The public IP address is fetched using the ipify API.
- Log files are stored in the `logs` directory, with daily rotation and backups for 15 days.

## License
This script is open-source and licensed under the MIT License.
