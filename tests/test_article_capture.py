"""Test the article_capture module"""

import requests
import pytest
import os
from requests_testadapter import Resp

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

def set_up():
    requests_session = requests.session()
    requests_session.mount('file://', LocalFileAdapter())
    response = requests_session.get('file://tests/test_src/sample_news.html')
    return response.status_code == 200

def test_page_Parse_provide_html():
    assert True

    
print(set_up())