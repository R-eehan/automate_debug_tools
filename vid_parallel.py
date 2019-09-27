from multiprocessing import Pool  # important: used in vid_parallel_download()
import requests

content_types = ['application/octet-stream; charset=utf-8', 'video/mp4; charset=utf-8']  # 2 birds, one stone.


def check_url(video_url_list):  # this fn performs the vid_url check

    with requests.get(video_url_list["video_url"], stream=True, timeout=5) as video_url_response_data:
            # print(video_url_response_data.headers)
            video_url_dict = {
                "hashed_id": video_url_list["hashed_id"],
                "os_version": video_url_list.get('os_version'),
                "os": video_url_list.get('os'),
                "browser": video_url_list.get('browser'),
                "browser_version": video_url_list.get('browser_version'),
                "reason": video_url_list.get('reason'),
                "build_name": video_url_list.get('build_name'),
                "session_name": video_url_list.get('session_name')
            }
            if video_url_response_data.headers['Content-Type'] in content_types:  # takes care of both AUT & AA
                video_url_dict["video"] = 'Yes'  # Updating the existing dictionary with a new key(video)
            else:
                video_url_dict["video"] = 'No'

            if video_url_response_data.headers['Content-Type'] == content_types[1]:  # for AA specifically
                del video_url_dict["browser"], video_url_dict["browser_version"]  # need to delete these keys
                video_url_dict.update(device= video_url_list.get('device'), app_name=video_url_list.get('app_name'),
                                      app_url=video_url_list.get('app_url'))  # replace the above keys with these for AA

    return video_url_dict


# using the multiprocessing module - https://chriskiehl.com/article/parallelism-in-one-line
def vid_parallel_download(thread, video_url_list):
    # thread and video_url_list is defined in vid_parser.py
    p = Pool(processes=thread)  # standard syntax in the multiprocessing module
    result = p.map(check_url, video_url_list)  # using map to store output in "result"
    # p.map = Pool(processes=thread).map(fn, iterable)

    return result
