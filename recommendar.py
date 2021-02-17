import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager
import yaml

class recommendar(object):
  email_list = pd.DataFrame(columns=['email', 'url'])

  def __init__(self):
    self.accquire_user_info()

  def scroll(self, url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options )

    driver.implicitly_wait(30)

    try:
        SCROLL_PAUSE_TIME = 5
        driver.get(url)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup

    finally:
        driver.quit()
  
  def goodreads_library_scrapper(self, account_name):
    url = 'https://www.goodreads.com/review/list/'+account_name+'?shelf=%23ALL%23'
    res = requests.get(url)
    content = self.scroll(url)#BeautifulSoup(res.content, "html.parser")
    # parse 
    books = []
    for tr in content.find_all('tr'):
        for td in tr.find_all('td', attrs={'class':'field title'}):
          for a in td.find_all('a'):
              books.append(a['title'])
    ratings = []
    for tr in content.find_all('tr'):
        for td in tr.find_all('td', attrs={'class':'field avg_rating'}):
          ratings.append(td.text.split()[2])
    my_ratings = []
    for tr in content.find_all('tr'):
        for td in tr.find_all('td', attrs={'class':'field shelves'}):
          for div in td.find_all('div', attrs={'class':'stars'}):
            my_ratings.append(div['data-rating'])   
    isbn = []
    for tr in content.find_all('tr'):
        for td in tr.find_all('td', attrs={'class':'field isbn'}):
          isbn.append(td.text.replace('isbn',''))
    dates = []
    for tr in content.find_all('tr'):
        for td in tr.find_all('td', attrs={'class':'field date_added'}):
          dates.append(td.text.replace('date','').replace('added',''))
    # construct dataframe
    lib_df = pd.DataFrame(list(zip(books,ratings, my_ratings, isbn, dates)), columns=['book', 'rating', 'my rating', 'isbn', 'date'])
    return lib_df      

  def recommendations_webscrapper(self, df):
    # sort and get isbns 
    count = (20 if df.shape[0]>20  else df.shape[0])
    df['date']= pd.to_datetime(df['date'])
    df = df.sort_values(['my rating', 'rating', 'date'], ascending=False)
    isbns = df['isbn'].iloc[0:count].replace('\n','')
    # web scrape
    books = []
    for i in range(count):
      if(not isbns.iloc[i] ==''):
        url ='https://www.whatshouldireadnext.com/isbn/'+isbns.iloc[i].strip()
        res = requests.get(url)
        content = BeautifulSoup(res.content, "html.parser") 
        for row in content.find_all('div', attrs={'class':'book-results__item'}):
          for book in row.find_all('h3', attrs={'class':'book-results__title'}):
            for auth in row.find_all('h4', attrs={'class':'book-results__author'}):
              books.append(book.text+' by '+auth.text)
          break
    # get result list 
    return [b.replace('\n', '') for b in books]
  
  def send_email(self, b, e):
    # set up the SMTP server
    My_address= self.email
    p = self.p
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(My_address, p)
    
    msg = MIMEMultipart()       # create a message

    # setup the parameters of the message
    msg['From']=My_address
    msg['To']= e
    msg['Subject']="This Month's Book recommendations"

    # add in the message body
    text ='This month\'s book recommendations:\n\n'
    i = 1
    for book in b:
      text += str(i)+'. '+ book + '\n'
      i += 1
    msg.attach(MIMEText(text, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    
    del msg

  def add_email(self, e, u):
    u = urlparse(u)
    if(u.netloc=="www.goodreads.com"):
      u = u.path
      u = u.replace("/user/show/", '')
      self.email_list = self.email_list.append({'email':e,'url': u}, ignore_index=True)
      self.activate(e,u)

  def activate(self, e, u):
    l= self.goodreads_library_scrapper(u)
    b= self.recommendations_webscrapper(l)
    self.send_email(b, e)

  def monthly_activate(self):
    for row in self.email_list.iterrows():
      self.activate(row[1]['email'],row[1]['url'])
  
  def accquire_user_info(self):
    conf = yaml.safe_load(open('conf/application.yml'))
    self.email = conf['email']
    self.p = conf['pass']