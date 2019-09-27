import csv
import sys
import logging
import json
from parallel_download import download
from setup import UPLOAD_FOLDER, DOWNLOAD_FOLDER, BROWSERSTACK_APP_AUT_SESSION_LOG_URL
from vid_parallel import vid_parallel_download

# essentially creating a logfile called "debug.log" for each functionality and saving it. This logfile logs all details.
# this is implemented for each functionality
LOG_FILENAME = 'debug.log'
format_string = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILENAME, format=format_string)       # look up the logging module


def file_to_meta_extractor(file):  # this is called in vid_parser_main()
    with open(UPLOAD_FOLDER + file) as csv_file:
        # print(csv_file)
        meta_info_list = list(csv.DictReader(csv_file, delimiter=',')) # converts uploaded csv data into a list of ordered dicts
    # print(meta_info_list)  # use this to see what is returned.
    return meta_info_list


def session_json_reader(file_path):  # used in vid_status_with_session(). Jump below
    with open(file_path, "r") as f:
        data = json.load(f)
        # print(data)
        # print(type(data))
        data = data['automation_session']
        # print(data)

    return data


def vid_status_with_session(meta_info_list):
    video_url_list = []

    for meta in meta_info_list:
        # meta_info_list = List of Ordered Dictionary.
        # Looping through each element in the list is essentially looping through a dictionary(keys).
        session_json = DOWNLOAD_FOLDER + meta['hashed_id'] + ".json"
        # meta["hashed_id] is us accessing the session ID.
        print(session_json)  # session_json is a FILE PATH with a .json extension.
        info = session_json_reader(session_json)  # the json file is passed to session_json_reader()
        video_url_dict = {
	        "hashed_id": meta['hashed_id'],
	        "video_url": info.get('video_url'),
	        "os": info.get('os'),
	        "os_version": info.get('os_version'),
	        "device": info.get('device'),
	        "app_name": info['app_details'].get('app_name'),
	        "app_url": info['app_details'].get('app_url'),
	        "reason": info.get('reason'),
	        "build_name": info.get('build_name'),
	        "session_name": info.get('name')
        }
        video_url_list.append(video_url_dict)
        # print(video_url_list)

    thread = 10
    video_url_dict_list = vid_parallel_download(thread, video_url_list)  # refer vid_parallel_download.py
    print(video_url_dict_list)

    return video_url_dict_list  # dict containing video(Yes/No) and hashed_id


def information_merge(meta_info_list):
    session_info_list = []
    video_url_dict_list = vid_status_with_session(meta_info_list)
    # print(video_url_dict_list)

    for meta in meta_info_list:
        session_dict = dict()  # simply creates dictionaries for each element in met_info_list.
        # print(session_dict)

        for key in meta.keys():
            session_dict[key] = meta[key]
        session_info_list.append(session_dict)
    # print(session_info_list)  # list of dicts: [{'hashed_id': <id>}, ..}

    # How to Merge Two Python Dictionaries - https://bit.ly/2MyVM48
    session_info_list = [dict(session_info_list[i], **video_url_dict_list[i]) for i in range(len(session_info_list))]
    # print(session_info_list)  # returns list of dicts: [{'hashed_id': <id>, 'video': Yes/No}
    return session_info_list


def app_aut_vid_parser_main(csv_fn):  # main function, calls file_to_meta() and information_merge()
    file_type = ".json"
    meta_info_list = file_to_meta_extractor(csv_fn)  # jump to file_to_meta_extractor()
    session_urls_list = [BROWSERSTACK_APP_AUT_SESSION_LOG_URL + meta['hashed_id'] + file_type for meta in meta_info_list]
    # print(session_urls_list)  # list of URLs,eg:'https://api-cloud.browserstack.com/app-automate/sessions/<s_id>.json'
    download(session_urls_list, DOWNLOAD_FOLDER)  # imported from parallel_download.py
    final_result = information_merge(meta_info_list)  # jump to information_merge()

    return final_result


if __name__ == '__main__':
    if len(sys.argv) == 2:
        csv_filename = sys.argv[1]
        app_aut_vid_parser_main(csv_filename)
    else:
        print("Usage: python3 vid_parser.py filename.csv")
