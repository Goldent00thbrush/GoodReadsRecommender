# Good Reads Book Recommender web app
A simple web-scrapping app built in Python and JavaScript.

## Introduction
The purpose of this project is to dive deeper into web scrapping and sending emails using SMTP. The idea is building a simple monthly recommendation mailing list. It recommends books based on the user’s Good Reads library. It simply picks out the top rated books by the user (or the genral rating if not rated) and uses them to get recommendations which are brought from https://www.whatshouldireadnext.com/.  The idea was inspired by my desire to have a monthly recommendation list based on my library. 
## The App
The front-end of the app can be seen here: https://goldent00thbrush.github.io/GoodReadsRecommender.github.io/ 
The backend is currently not hosted. 
## Technologies 
-	Beautifulsoup4 4.9.3
-	Flask 1.1.2
-	HTML 5
-	Javascript 
-	Python 3.8.5
-	Requests 2.25.1
-	Selenium 3.141.0
-	Yaml 0.2.5
## Setup
1.	Download the repo.
2.	Place your email and password to be used in conf/application.yml 
3.	Run app.py (python app.py)
4.	Open https://goldent00thbrush.github.io/GoodReadsRecommender.github.io/
## Features/Components 
-	A Good Reads web scrapper
o	Uses the selenium package along with the chrome driver to scrape the scrollable Good Reads library. 
-	A What Should I read next
-	A SMTP server 
## Status 
The project is done. It took around 16 hours to develop (4 hours per week for 4 weeks).
## Future development
If the development of this project picks up again, here are things I want to work on or improve:
-	Manage the storage of passwords when the code is running.
-	A more friendly UI.
-	A bit more logic regarding generating the recommendations.
-	A database to store and manage the mailing lists. 
## Acknowledgments 
-	The styling css file was adopted from https://codepen.io/dope/pen/ZQWBeL 
-	The loader was adopted from https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_loader
## License 
The source code for this project is licensed under the MIT license, which you can find in the MIT-LICENSE.txt file.
## Contact
Created by @goldent00thbrush - feel free to contact me!



