from deta import Deta
import io
import os
import datetime
from datascrap import ScrapDev
from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup
from deta import app


load_dotenv(find_dotenv())

urls = os.environ.get("URL")
project_key = os.environ.get("PROJECTKEY")
current_date = datetime.datetime.now()
folder_date=current_date.strftime("%x")
new_folder_date=folder_date.replace("/", "_")




deta = Deta(project_key)
folder_name = f"blogs"
drive = deta.Drive(folder_name)
blog = ScrapDev(urls)


@app.lib.run(action="blogs")
@app.lib.cron()
def blogs_scrapping(event):

    try:
        
        for key, value in blog:
            
            res=requests.get(str(value)).text.encode('utf8').decode('ascii', 'ignore')
            soup=BeautifulSoup(res, "html.parser")
            find_title=soup.find("h1")
            find_tags=soup.find("div", class_="spec__tags flex flex-wrap")
            find_article=soup.find("div", class_="crayons-article__main")
            title=' '.join(find_title.text.strip().split())
            tags=find_tags.text
            article=find_article.text

            with io.StringIO() as f:
                f.write(f"{key, value}")
                f.write("\n")
                f.write(str(find_title))
                f.write("\n")
                f.write("\n Tags")
                f.write(str(find_tags))
                f.write("\n Article")
                f.write(str(find_article))
                print(drive)

                drive.put(f"{key}.md", f.getvalue())

        return "Scrapped Successfully"

    except Exception as e: 
        print(e)

