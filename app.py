# -*- coding: utf-8 -*-
# Comments
# Libraries
import telnetlib
import uao_decode
import sys
import datetime
import time
import re
import http.client
from bs4 import BeautifulSoup
# Global setup definition
bm_list = ['yukinoba', 'frojet'];
login = {'account': 'yukinoba', 'password': 'ckmagic007'};
# Function definition
# Utility: convert PTT web filename to AIDu
def fn2aidu( type, v1, v2 ):
    # print(">>> type=" + str(type));
    # print(">>> v1=" + str(v1));
    # print(">>> v2=" + str(v2));
    aidu = None;
    type_int = 0;
    if type == "G":
        type_int = 1;
    v1_int = 0;
    if not v1 is None:
        v1_int = int(v1, 10);
    v2_int = 0;
    if not v2 is None:
        v2_int = int(v2, 16);
    aidu = ((type_int & 0xf) << 44) | ((v1_int & 0xffffffff) << 12) | (v2_int & 0xfff);
    return aidu;
# Utility: convert PTT AIDu to AIDc
def aidu2aidc( aidu ):
    # print(">>> aidu=" + str(aidu));
    aidc = None;
    aidc_cell = ['X','X','X','X','X','X','X','X'];
    aidc_map = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','-','_'];
    if not aidu is None:
        aidu_tmp = aidu;
        for cell_index in range(7, -1, -1):
            map_index = aidu_tmp % len(aidc_map);
            aidc_cell[cell_index] = aidc_map[map_index];
            aidu_tmp = aidu_tmp // len(aidc_map);
    aidc = ''.join(aidc_cell);
    return aidc;
# Main procedure
# Work until shutdown
while True:
    # # TODO: crawler for Twitter
    # conn = http.client.HTTPSConnection("www.ptt.cc");
    # conn.request("GET", "/bbs/ONE_PIECE/index.html");
    # response_list = conn.getresponse();
    # content_list = response_list.read().decode(response_list.headers.get_content_charset('utf-8'));
    # # TODO: find the news post
    # # TODO: update the news post
    # # Close connection
    # conn.close();
    # # Rest a moment
    # #--2017.10.05 extends to 3mins a round
    # time.sleep(60 * 3);