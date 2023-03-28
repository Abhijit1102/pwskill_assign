from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin

from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests
import re



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
             
            url = "https://www.youtube.com/@PW-Foundation/videos"

            html = requests.get(url).text

            video_ids = re.findall(r"watch\?v=(\S{11})", html)

            video_links = ["https://www.youtube.com/watch?v=" + id for id in video_ids]

            urls = video_links[:5]

            urls

            
            thumbnails_links = []

            for url in urls:

                # Extract video ID from URL
                exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
                s = re.findall(exp, url)[0][-1]

                # Construct image URL
                thumbnail_url = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

                thumbnails_links.append(thumbnail_url)  

            titles = []
            views = []
            times = []   
            def give_me_everything():

                data = soup.find_all("meta") 

                for i in range(len(data)):  
                    print(data[i])

            for url  in urls:
            
                session = HTMLSession() 
                response = session.get(url)  

                if response.status_code != 200: 
                    print("Error! Response = " + str(response.status_code))
                else:
                    soup = bs(response.content, "html.parser")  
                    title =  soup.find("meta", property="og:title")["content"]
                    titles.append(title)


            for url in urls:
            
                session = HTMLSession() 
                response = session.get(url)  

                if response.status_code != 200: 
                    print("Error! Response = " + str(response.status_code))
                else:
                    soup = bs(response.content, "html.parser")  
                    view =  soup.find("meta", itemprop="interactionCount")["content"]
                    views.append(view)


            for url in urls:
   
                session = HTMLSession() 
                response = session.get(url)  

                if response.status_code != 200: 
                    print("Error! Response = " + str(response.status_code))
                else:
                    soup = bs(response.content, "html.parser")  
                    time = soup.find("meta", itemprop="uploadDate")["content"]
                    times.append(time)
                
            mydict = {"urls": urls, "thumbnails_links": thumbnails_links, 
                      "titles": titles, "views": views,
                    "time": times}
            reviews= []
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
