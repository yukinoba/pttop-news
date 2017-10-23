# -*- coding: utf-8 -*-
# Comments
# Libraries
import telnetlib
import uao_decode
import sys
import datetime
from datetime import timedelta
import time
import re
import http.client
from bs4 import BeautifulSoup
import tweepy
# Global setup definition
bm_list = ['yukinoba', 'frojet'];
login = {'account': 'yukinoba', 'password': 'ckmagic007'};
# Twitter application consumer keys
# https://apps.twitter.com/
twitter_consumer_key = 'rn9drYLjeSxrnUjq22J9Bmaq0';
twitter_consumer_secret = 'wMy9iId8y9BkVz0vm0R0a2Zx3lNupRDYKJ1ijYQtZzNDgwAUHP';
twitter_access_token = '280778178-ZMLPmD81pcn83lrCGI9PLCRDKw2uKoOgF8guV2uO';
twitter_access_token_secret = 'BVoPitNWsmfAEXySLVyexRLBMXGFxdcGohFqtqjSnL6YL';
# ONE_PIECE twitters
twitter_userids = ['OPcom_info', 'Eiichiro_Staff', 'mugistore_info', 'ONEPIECE_trecru', 'opgame_official', '1kuji_onepiece', 'onepiecetower'];
# ONE_PIECE last tweets record
last_tweetids = {};
for twitter_userid in twitter_userids:
    last_tweetids[twitter_userid] = 0;
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
# Utility: handle Tweepy twitter API limits
def limit_handled( cursor ):
    while True:
        try:
            yield cursor.next();
        except tweepy.TweepError:
            time.sleep(60 * 15);
# Main procedure
# Work until shutdown
while True:
    tweets = [];
    # Crawler for Twitter
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret);
    auth.set_access_token(twitter_access_token, twitter_access_token_secret);
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True);
    # Get today news only
    nowdatetime = datetime.datetime.utcnow() + datetime.timedelta(hours=8);
    today = datetime.datetime.combine(nowdatetime.date(), datetime.time.min);
    for userid in twitter_userids:
        latest_tweetid = last_tweetids[userid];
        # Get certain twitter users last 10 status
        for status in limit_handled(tweepy.Cursor(api.user_timeline, id=userid, page=1, tweet_mode='extended').items(10)):
            # Get today news only and keep tracking only the latest news
            if status.created_at + datetime.timedelta(hours=8) > today and status.id > latest_tweetid:
                if hasattr(status, 'retweeted_status') or status.full_text.startswith("RT"):
                    pass
                else:
                    tweet = {};
                    tweet['time'] = status.created_at + datetime.timedelta(hours=8);
                    # Get original tweet links
                    olink_index = status.full_text.rfind("http://");
                    if olink_index > 0:
                        tweet['link'] = status.full_text[olink_index:];
                        tweet['content'] = status.full_text[:olink_index];
                    else:
                        tweet['link'] = "";
                        tweet['content'] = status.full_text;
                    tweet['imgurls'] = [];
                    try :
                        if 'media' in status.extended_entities:
                            for media in status.extended_entities['media']:
                                if media['type'] == 'photo':
                                    tweet['imgurls'].append(media['media_url']);
                    except AttributeError:
                        pass
                    if status.id > last_tweetids[userid]:
                        last_tweetids[userid] = status.id;
                    tweets.append(tweet);
    for tweet in tweets:
        print(str(tweet['time']));
        print(str(tweet['link']));
        print(str(tweet['content']));
        for imgurl in tweet['imgurls']:
            print(str(imgurl));
        print("-----------------------------------------");
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
    time.sleep(60 * 15);