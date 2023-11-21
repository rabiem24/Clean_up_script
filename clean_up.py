#!/usr/bin/env python3

import argparse
import subprocess
import logging
from datetime import datetime

# Use the absolute path.
# Use the format YYYY-mm-dd for the dates

date_today = datetime.now().date().strftime("%Y-%m-%d")

def initialize_command(path, file_type=None, start_date=None, end_date=None):     
    command = ""


    if (file_type != None and file_type != "") and (start_date != None and start_date != "") and (end_date != None and end_date != ""):

        command = f'find {path} -type f -name "*.{file_type}" -newermt "{start_date}" ! -newermt "{end_date}" -exec rm -f {{}} \;'
    
    elif (file_type != None and file_type != "") and (start_date != None and start_date != ""):

        command = f'find {path} -type f -name "*.{file_type}" -newermt "{start_date}" ! -newermt "{date_today}" -exec rm -f {{}} \;'

    elif (file_type != None and file_type != "") and (end_date != None and end_date != ""):

        command = f'find {path} -type f -name "*.{file_type}" -newermt "{end_date}" -exec rm -f {{}} \;'

    elif (start_date != None and start_date != "") and (end_date != None and end_date != ""):

        command = f'find {path} -type f -newermt "{start_date}" ! -newermt "{end_date}" -exec rm -f {{}} \;'

    elif (start_date != None and start_date != ""):

        command = f'find {path} -type f -newermt "{start_date}" ! -newermt "{date_today}" -exec rm -f {{}} \;'

    elif (end_date != None and end_date != ""):

        command = f'find {path} -type f -newermt "{end_date}" -exec rm -f {{}} \;'

    elif (file_type != None and file_type != ""):

        command = f'find {path} -type f -name "*.{file_type}" -exec rm -f {{}} \;'

    else:

        command = f'find {path} -type f -exec rm -f {{}} \;'

    return command
    

def test_files(path, file_type=None, start_date=None, end_date=None):

    date_today = datetime.now().date().strftime("%Y-%m-%d")

    if (file_type != None and file_type != "") and (start_date != None and start_date != "") and (end_date != None and end_date != ""):

        command = f'find {path} -type f -name "*.{file_type}" -newermt "{start_date}" ! -newermt "{end_date}" -print'
    
    elif (file_type != None and file_type != "") and (start_date != None and start_date != ""):

        command = f'find {path} -type f -name "*.{file_type}" -newermt "{start_date}" ! -newermt "{date_today}" -print'

    elif (file_type != None and file_type != "") and (end_date != None and end_date != ""):

        command = f'find {path} -type f -name "*.{file_type}" -newermt "{end_date}" -print'

    elif (start_date != None and start_date != "") and (end_date != None and end_date != ""):

        command = f'find {path} -type f -newermt "{start_date}" ! -newermt "{end_date}" -print'

    elif (start_date != None and start_date != ""):

        command = f'find {path} -type f -newermt "{start_date}" ! -newermt "{date_today}" -print'

    elif (end_date != None and end_date != ""): 

        command = f'find {path} -type f -newermt "{end_date}" -print'

    elif (file_type != None and file_type != ""):

        command = f'find {path} -type f -name "*.{file_type}" -print'



def main():
    parser = argparse.ArgumentParser("Cleanup Script for linux")        #Setting arguments for the script

    #Add arguments here
    parser.add_argument('path', help='Path of files to be deleted. Please use thye absolute path.')
    parser.add_argument('--file_type', '-t', help='File extensions to be deleted')
    parser.add_argument('--start_date', '-s', help='Starting date of the range of files to delete (Format: mm-dd-YYYY)')
    parser.add_argument('--end_date', '-e', help='End date of the range of files to delete (Format: mm-dd-YYYY)')
    parser.add_argument('--log', '-l', help='Log path')

    args = parser.parse_args()


    path = args.path
    file_type = args.file_type
    start_date = args.start_date
    end_date = args.end_date
    log_file_path = args.log


    # Configure the logging module
    if log_file_path != None and log_file_path != "":
        logging.basicConfig(level=logging.INFO)

        # Create a FileHandler to write log messages to a file
        log_file = f'{log_file_path}/clean_up_log_{date_today}'
        file_handler = logging.FileHandler(log_file)

        # Create a formatter to specify the log message format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the FileHandler to the logger
        logger = logging.getLogger(__name__)
        logger.addHandler(file_handler)
    

    try: 

        # Command final
        command = initialize_command(path, file_type, start_date, end_date)

        # Run the command and capture output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Log the standard output
        logger.info("Command Result: \n%s", result.stdout)

    except subprocess.CalledProcessError as e:
        # Log the error and error output
        logger.error("Error running command: %s", e)
        logger.error("Command returned non-zero exit code: %s", e.returncode)
        logger.error("Error output:\n%s", e.stderr)

if __name__ == "__main__":

    main()

# Run command example 
# python3 clean_up.py /home/rabiem24/Documents/files -t exe -s 2023-08-01 -e 2023-10-13 -l /home/rabiem24/Documents/logs
#  ./clean_up.py /home/rabiem24/Documents/files --file_type exe --start_date 2023-08-01 --end_date 2023-10-13 -l /home/rabiem24/Documents/logs

