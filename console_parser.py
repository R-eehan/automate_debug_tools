import csv
import sys
import json
import datetime
import logging
from logs_parallel import download
from setup import UPLOAD_FOLDER, DOWNLOAD_FOLDER, BROWSERSTACK_AUT_SESSION_LOG_URL

LOG_FILENAME = 'debug.log'
format_string = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILENAME, format=format_string)


def file_to_meta_extractor(file):
    with open(UPLOAD_FOLDER + file) as csv_file:
        meta_info_list = list(csv.DictReader(csv_file, delimiter=','))

    return meta_info_list


def console_log_reader(console_log_path):
    with open(console_log_path, "r") as f:
        data = f.readlines()

    return data


def console_log_searcher(console_raw_info, stext):

    for line in console_raw_info:
        if stext in line:
            return True


def information_merge(meta_info_list, stext):
    session_info_list = []
    session_dict = dict()

    for meta in meta_info_list:
        console_log_path = DOWNLOAD_FOLDER + meta['hashed_id']
        console_raw_info = console_log_reader(console_log_path)

        if console_log_searcher(console_raw_info, stext):
            for key in meta.keys():
                session_dict[key] = meta[key]
            session_info_list.append(session_dict)

    return session_info_list


def console_parser_main(csv_fn, stext):
    meta_info_list = file_to_meta_extractor(csv_fn)
    console_log_urls_list = [BROWSERSTACK_AUT_SESSION_LOG_URL + meta['hashed_id'] + "/consolelogs" for meta in meta_info_list]
    download(console_log_urls_list, DOWNLOAD_FOLDER)
    final_result = information_merge(meta_info_list, stext)

    return final_result


if __name__ == '__main__':
    if len(sys.argv) == 3:
        csv_filename = sys.argv[1]
        search_text = sys.argv[2]
        console_parser_main(csv_filename, search_text)
    else:
        print("Usage: python3 command_parser.py filename.csv 'search text'")
