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
import unicodedata
# Global setup definition
bm_list = ['yukinoba', 'frojet'];
login = {'account': 'SeptemberCat', 'password': 'meow'};
# Twitter application consumer keys
# https://apps.twitter.com/
twitter_consumer_key = 'rn9drYLjeSxrnUjq22J9Bmaq0';
twitter_consumer_secret = 'wMy9iId8y9BkVz0vm0R0a2Zx3lNupRDYKJ1ijYQtZzNDgwAUHP';
twitter_access_token = '280778178-ZMLPmD81pcn83lrCGI9PLCRDKw2uKoOgF8guV2uO';
twitter_access_token_secret = 'BVoPitNWsmfAEXySLVyexRLBMXGFxdcGohFqtqjSnL6YL';
# ONE_PIECE twitters
twitter_userids = ['OPcom_info', 'Eiichiro_Staff', 'mugistore_info', 'ONEPIECE_trecru', 'opgame_official', '1kuji_onepiece', 'onepiecetower'];
twitter_usernames = {'OPcom_info': "ONE PIECE 綜合官方誌", 'Eiichiro_Staff': "ONE PIECE 編輯部", 'mugistore_info': "草帽商店", 'ONEPIECE_trecru': "航海王：秘寶尋航", 'opgame_official': "ONE PIECE 家用主機遊戲", '1kuji_onepiece': "航海王一番賞", 'onepiecetower': "東京鐵塔航海王主題樂園"};
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
# Function: post or update twitter news
def news_update( newslink, tweets ):
    tn = telnetlib.Telnet('ptt.cc');
    time.sleep(3);
    content_term = tn.read_very_eager().decode('uao_decode');
    # Login process
    if "請輸入代號" in content_term:
        print(">>> 輸入帳號");
        tn.write(login['account'].encode('uao_decode') + b"\r");
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        # Enter password
        if "請輸入您的密碼" in content_term:
            print(">>> 輸入密碼");
            tn.write(login['password'].encode('uao_decode') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
            # Duplicated login record
            if "您想刪除其他重複登入的連線嗎" in content_term:
                print(">>> 刪除重複登入");
                tn.write("n".encode('uao_decode') + b"\r");
                time.sleep(5);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Busy login
            if "請勿頻繁登入" in content_term:
                print(">>> 頻繁登入");
                tn.write(" ".encode('uao_decode') + b"\r");
                time.sleep(5);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Temporary login waiting
            if "登入中" in content_term:
                print(">>> 等待登入");
                tn.write(" ".encode('uao_decode'));
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Dashboard
            if "請按任意鍵繼續" in content_term:
                print(">>> 登入成功");
                tn.write(" ".encode('uao_decode'));
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Unfinished post
            if "尚未完成" in content_term:
                print(">>> 未完發文");
                tn.write("q".encode('uao_decode') + b"\r");
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
    # Enter specific board
    if "主功能表" in content_term:
        print(">>> 主功能表");
        tn.write("s".encode('uao_decode'));
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        # Choose board
        if "選擇看板" in content_term:
            print(">>> 選擇看板");
            # tn.write("ONE_PIECE".encode('uao_decode') + b"\r");
            tn.write("Test".encode('uao_decode') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
            # Board entry
            if "動畫播放中" in content_term:
                print(">>> 進板畫面");
                tn.write("q".encode('uao_decode'));
                time.sleep(3);
                content_term = tn.read_very_eager().decode('uao_decode');
            # Post list
            if "文章選讀" in content_term:
                print(">>> 文章列表");
                # Go to the post
                postlist = [newslink];
                for postlink in postlist:
                    if not postlink == "":
                        # Convert web BBS postlink filename to telnet BBS post AIDc
                        aidc = None;
                        pattern = re.compile('\/([MG]{1})\.([0-9]+)\.A\.([0-9A-F]+)\.html');
                        mo = re.search(pattern, postlink);
                        if mo:
                            type = mo.group(1);
                            v1 = mo.group(2);
                            v2 = mo.group(3);
                            aidc = aidu2aidc(fn2aidu(type, v1, v2));
                        if aidc is None:
                            continue;
                        tn.write("#".encode('uao_decode'));
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Jump to post by AID
                        if "文章代碼" in content_term:
                            print(">>> 跳至文章：" + "#" + aidc);
                            tn.write(aidc.encode('uao_decode') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Post not exists
                            if "請按任意鍵繼續" in content_term:
                                print(">>> 沒有文章");
                                tn.write(" ".encode('uao_decode'));
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                # Back to post list
                                continue;
                            #--2017.09.29 After post jump, there is no "文章選讀" keywords
                            #--2017.09.29 redraw the terminal content
                            tn.write(b"\x1b[C");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            tn.write(b"\x1b[D");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Edit the existed post
                            if "文章選讀" in content_term:
                                print(">>> 編輯文章");
                                tn.write("E".encode('uao_decode'));
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                    else:
                        print(">>> 發表文章");
                        tn.write(b"\x10");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Create a new post
                        if "發表文章" in content_term:
                            # Customize post category
                            if "種類" in content_term:
                                print(">>> 自訂分類");
                                tn.write(b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                # News post title
                                if "標題" in content_term:
                                    print(">>> 輸入標題");
                                    nowdatetime = datetime.datetime.utcnow() + datetime.timedelta(hours=8);
                                    today = datetime.datetime.combine(nowdatetime.date(), datetime.time.min);
                                    tn.write(("[情報] " + today.strftime('%m/%d') + " 最新情報匯整").encode('uao_decode') + b"\r");
                                    time.sleep(3);
                                    content_term = tn.read_very_eager().decode('uao_decode');
                    # Edit the post
                    if "編輯文章" in content_term:
                        print(">>> 編輯文章");
                        tn.write(b"\x13");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Search for the top-lined keyword
                        if "[搜尋]" in content_term:
                            tn.write("依時間順，最新情報顯示於最上方：".encode('uao_decode') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Caps or not
                            if "區分大小寫" in content_term:
                                tn.write("y".encode('uao_decode') + b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                        # Clear top-line and create edit area
                        tn.write(b"\x19");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        tn.write("依時間順，最新情報顯示於最上方：".encode('uao_decode') + b"\r");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        tn.write(b"\r");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        for tweet in tweets:
                            print(">>> 更新情報");
                            print(str(tweet['time']) + str(tweet['link']));
                            print(str(tweet['content']));
                            for imgurl in tweet['imgurls']:
                                print(str(imgurl));
                            tn.write(("※ " + tweet['name'] + " " + str(tweet['time'])).encode('uao_decode') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            tn.write(("原文網址：" + tweet['link']).encode('uao_decode') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Write whole texts
                            tn.write(str(tweet['content']).encode('uao_decode'));
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # # Ideal width of single post line is 50 half-width chars
                            # line_limit = 50;
                            # counter = 0;
                            # for char in tweet['content']:
                                # tn.write(char.encode('uao_decode'));
                                # time.sleep(3);
                                # content_term = tn.read_very_eager().decode('uao_decode');
                                # charwidth = unicodedata.east_asian_width(char);
                                # if charwidth in ['F', 'W']:
                                    # counter = counter + 2;
                                # elif charwidth in ['A', 'H', 'N', 'Na']:
                                    # counter = counter + 1;
                                # else:
                                    # counter = counter + 1;
                                # if counter > line_limit:
                                    # counter = 0;
                                    # tn.write(b"\r");
                                    # time.sleep(3);
                                    # content_term = tn.read_very_eager().decode('uao_decode');
                            # if counter > 0:
                                # tn.write(b"\r");
                                # time.sleep(3);
                                # content_term = tn.read_very_eager().decode('uao_decode');
                            # Images in tweet
                            for imgurl in tweet['imgurls']:
                                tn.write(imgurl.encode('uao_decode') + b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                            # End of a tweet
                            tn.write(b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                        # End of for-loop
                        tn.write(b"\x18");
                        time.sleep(3);
                        content_term = tn.read_very_eager().decode('uao_decode');
                        # Save edited post
                        if "檔案處理" in content_term:
                            print(">>> 儲存編輯");
                            tn.write("s".encode('uao_decode') + b"\r");
                            time.sleep(3);
                            content_term = tn.read_very_eager().decode('uao_decode');
                            # Signature
                            if "簽名檔" in content_term:
                                print(">>> 加簽名檔");
                                tn.write("1".encode('uao_decode') + b"\r");
                                time.sleep(3);
                                content_term = tn.read_very_eager().decode('uao_decode');
                                # Done
                                if "請按任意鍵繼續" in content_term:
                                    print(">>> 完成編輯");
                                    tn.write(b"\r");
                                    time.sleep(3);
                                    content_term = tn.read_very_eager().decode('uao_decode');
    # Logout process
    while not "主功能表" in content_term:
        print(">>> 回上一層");
        tn.write(b"\x1b[D");
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
    if "主功能表" in content_term:
        print(">>> 登出");
        tn.write(b"\x1b[D");
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        tn.write(b"\x1b[C");
        time.sleep(3);
        content_term = tn.read_very_eager().decode('uao_decode');
        # Confirm logout
        if "您確定要離開" in content_term:
            print(">>> 確認登出");
            tn.write("Y".encode('uao_decode') + b"\r");
            time.sleep(3);
            content_term = tn.read_very_eager().decode('uao_decode');
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
                    # Ignore retweeted posts
                    pass
                else:
                    print(">>> 有新情報");
                    tweet = {};
                    tweet['name'] = twitter_usernames[userid];
                    tweet['time'] = status.created_at + datetime.timedelta(hours=8);
                    # Original tweet links
                    tweet['link'] = "https://twitter.com/" + userid + "/status/" + str(status.id);
                    tweet['content'] = status.full_text;
                    # Get any images in the tweet
                    tweet['imgurls'] = [];
                    try :
                        if hasattr(status.extended_entities, 'media'):
                            for media in status.extended_entities['media']:
                                if media['type'] == 'photo':
                                    tweet['imgurls'].append(media['media_url']);
                    except AttributeError:
                        # Ignore error
                        pass
                    if status.id > last_tweetids[userid]:
                        last_tweetids[userid] = status.id;
                    tweets.append(tweet);
    # Sort tweets by created_at time descending sequence
    tweets.sort(key=lambda tweet: tweet['time'], reverse=True);
    if len(tweets) > 0:
        conn = http.client.HTTPSConnection("www.ptt.cc");
        # conn.request("GET", "/bbs/ONE_PIECE/index.html");
        conn.request("GET", "/bbs/Test/index.html");
        response_list = conn.getresponse();
        content_list = response_list.read().decode(response_list.headers.get_content_charset('utf-8'));
        # Find the post
        post_href = "";
        in_nowday = True;
        endoflist = False;
        while not endoflist and in_nowday and post_href == "":
            soup_list = BeautifulSoup(content_list, 'html.parser');
            for postentry in soup_list.select('div.r-ent'):
                postdate = postentry.select('div.date')[0].text.strip();
                postauthor = postentry.select('div.author')[0].text;
                if datetime.datetime.strptime(postdate, "%m/%d").date() == today.date() and postauthor.strip() == login['account']:
                    # Get post link
                    for postlink in postentry.select('div.title > a'):
                        post_href = postlink['href'];
                if datetime.datetime.strptime(postdate, '%m/%d').date() < today.date():
                    # Has no post today
                    in_nowday = False;
            # Get previous page link
            prevpage_href = "";
            for button in soup_list.select('a.btn'):
                if "上頁" in button.text and hasattr(button, 'href'):
                    prevpage_href = button['href'];
            # End of list
            if prevpage_href == "":
                endoflist = True;
            else:
                # Go to previous page
                conn.request("GET", prevpage_href);
                response_list = conn.getresponse();
                content_list = response_list.read().decode(response_list.headers.get_content_charset('utf-8'));
        # Close connection
        conn.close();
        # Update tweets to existed post or create a new post
        news_update(post_href, tweets);
    # Rest a moment
    #--2017.10.05 extends to 15mins a round for Twitter APIs rate limit
    time.sleep(60 * 15);