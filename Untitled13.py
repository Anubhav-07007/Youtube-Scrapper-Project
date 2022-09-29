#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask,request,render_template,jsonify
from flask_cors import CORS , cross_origin
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

app=Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()

def homepage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()


def index():
    if request.method=="POST":
        try:
            def scroll_to_end(driver, sleep_between_interactions):
                """
                :param wd: give driver name {"wd = webdriver.Chrome()" and "wd = webdriver.FirefoxOptions()"}
                :param sleep_between_interactions: fix the time sleep value according to your network connection
                :return: scroll down to the end of your page
                """
                prev_h = 0
                for i in range(20):
                    driver.execute_script("window.scrollTo(0,(window.pageYOffset+300))")
                    height = driver.execute_script("""
                                function getActualHeight() {
                                    return Math.max(
                                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                                    );
                                }
                                return getActualHeight();
                            """)
                    driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
                    # fix the time sleep value according to your network connection
                    time.sleep(sleep_between_interactions)
                    prev_h += 200
                    if prev_h >= height:
                        break


            link = 'https://www.youtube.com/user/krishnaik06/videos'

            #chrome_options = Options()
            #chrome_options.add_argument("--headless")
            #driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome()
            driver.get('{}'.format(link))
            driver.maximize_window()
            scroll_to_end(driver, 1)
            content = driver.page_source.encode('utf8')
            soup = BeautifulSoup(content, 'lxml')
            driver.close()



            video_title = soup.find_all('h3', {'class': 'style-scope ytd-grid-video-renderer'})
            video_view = soup.find_all('span', {'style-scope ytd-grid-video-renderer'})
            video_url = soup.find_all('a', id='video-title')
            link = 'https://www.youtube.com'
            create_thumbnail_link = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'
            channel_video_url = []
            title = []
            view = []
            post_time = []
            thumbnail_link = []

            for i in video_title:
                title.append(i.text)

            for i in video_url:
                channel_video_url.append(link + i['href'])

            for i in range(len(video_view)):
                if i % 2 == 0:
                    view.append(video_view[i].text)
                else:
                    post_time.append(video_view[i].text)
            thumbnail = []
            for i in video_url:
                thumbnail.append(i['href'].split('='))
            thumbnail_id = []
            for i in thumbnail:
                if len(i) == 2:
                    thumbnail_id.append(i[1])
                else:
                    pass
            for i in thumbnail_id:
                thumbnail_link.append(create_thumbnail_link.format(i))

            data = []


            for i in range(50):
                channel_video_url, title, view, post_time, thumbnail_link
                mydict = {'video_title': title[i], 'views': view[i], 'posted_time': post_time[i],
                          'channel_video_url': channel_video_url[i],
                          'thumbnail_image_link': thumbnail_link[i]}


                data.append(mydict)
            return render_template('results.html',reviews=data)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return  render_template("index.html")

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(port=5000, debug=True)


# In[ ]:




