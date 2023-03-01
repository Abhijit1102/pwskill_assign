from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin

import requests
import re
import os
import time 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from urllib.request import urlopen as uReq
import pymongo

application = Flask(__name__) # initializing a flask app
app=application

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")
@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
             
            reviews = []   
            options = Options()
            driver = webdriver.Firefox(options=options)

            driver.implicitly_wait(5)

            driver.get(f"https://www.youtube.com/@{searchString}/videos")
            time.sleep(5)
            allchannellist = driver.find_elements(By.CSS_SELECTOR, "a#video-title-link")
                
            urls = list(dict.fromkeys(map(lambda a : a.get_attribute("href"), allchannellist)))
            driver.quit()
            urls = urls[:5]

            
            thumbnails_links = []

            for i in urls:
                url = i
                exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
                s = re.findall(exp,url)[0][-1]
                thumbnail = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

                #image scraping
                def imagedown(url, folder):
                    try:
                        os.mkdir(os.path.join(os.getcwd(), folder))
                    except:
                        pass
                    os.chdir(os.path.join(os.getcwd(), folder))

                    name = url
                    link = url
                    with open(name.replace(' ', '-').replace('/', '') + '.jpg', 'wb') as f:
                        im = requests.get(link)
                        f.write(im.content)
                        #print( name)
                        thumbnails_links.append(name)

                imagedown(thumbnail, 'image')

                
            driver = webdriver.Firefox( options=options)

            driver.implicitly_wait(5)


            driver.get(f"https://www.youtube.com/@{searchString}/videos")
            time.sleep(5)
            all_titles = driver.find_elements(By.CSS_SELECTOR, "a#video-title-link")
            titles = [title.get_attribute('title') for title in all_titles]
            driver.quit()
            titles= titles[:5]

            driver = webdriver.Firefox(options=options)

            driver.implicitly_wait(5)
            driver.get(f"https://www.youtube.com/@{searchString}/videos")
            time.sleep(5)
            allchannellist = driver.find_elements(By.CSS_SELECTOR, "span.style-scope.ytd-video-meta-block")
            views_time = list(dict.fromkeys(map(lambda a : a.get_attribute("innerHTML"), allchannellist)))
            driver.quit()
            views_time = views_time[0:11]
            views =[i  for i in views_time if i.endswith("views")]

            driver = webdriver.Firefox(options=options)

            driver.implicitly_wait(5)
            driver.get(f"https://www.youtube.com/@{searchString}/videos")
            #time.sleep(5)
            allchannellist = driver.find_elements(By.CSS_SELECTOR, "span.style-scope.ytd-video-meta-block")
            views_time = list(dict.fromkeys(map(lambda a : a.get_attribute("innerHTML"), allchannellist)))
            driver.quit()
            views_time = views_time[0:11]
            times = [i  for i in views_time if not i.endswith("views")]
            mydict = {"urls": urls, "thumbnails_links": thumbnails_links, 
                      "titles": titles, "views": views,
                    "time": times}
            
            reviews.append(mydict)

            return render_template('results.html', reviews=reviews)
        
        except Exception as e:
            print('The Exception message is: ', e)
            return f'something is wrong: {e}'
    

    else:
        return render_template('index.html')
    

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
	#app.run(debug=True)
