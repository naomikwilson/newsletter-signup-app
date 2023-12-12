# newsletter-signup-app
### Team members: Naomi Wilson and Justine Zhao

## Project Overview 

Our web application generates recommendations for newsletters based on the categories that the user selects; the user creates an account to generate and save their recommendations and can log in later to save additional recommendations or remove current ones from their list. We also have a random fact on the homepage about a historical event that took place on the day and month that the user visits our app. We also hope that more people can reap the benefits of reading news by getting rid of the fear of forgetting which newsletters they subscribed to. 


## Usage Guidelines  

Upon visiting our site, the user can learn more about us or they can go straight into logging in or creating through the buttons under the introduction paragraph. After logging in or creating an account, the user will be taken to the matches page where they can select one or more categories of newsletters that they would like to be recommended. After pressing the submit button, the user can then add newsletters to their list. If they have added newsletters during a previous session, they will also have the option to remove newsletters from their list. The user can move between our pages by utilizing the menu dropdown button in the top right corner of the page.  


## Dependencies 

The main component of our app, the newsletter recommendation feature, uses a combination of Flask, sqlite3, a newsletter data dictionary, and a “newsletter.db” database. Flask is used to integrate the back-end and front-end aspects of our app using features such as route, get, post, redirect, render_template, request, g (database management), and flash (displaying error messages – requires a special key). Sqlite3 is used to retrieve information from or update the newsletter.db database when a user creates a new account, logs in, or selects newsletters that they want to add/remove from their list. The newsletter data dictionary contains the newsletter names and links corresponding to each of the 7 categories (Current Events, Finance and Markets, Food and Agriculture, Sustainability and the Environment, Science, Health and Medicine, Education) and is used as our primary data source for the project. We also used libraries such as OS (generate secret key), requests and json (for retrieving the data from the API), random, datetime, and hashlib (hashing the passwords). For the historical events generation component of our app, we used API ninjas as an external resource to get the API key and the random historical fact on the home page (https://api-ninjas.com/api/historicalevents). 


## Project Structure and Collaboration 

In terms of project structure, the main folders for the front-end were static and templates, because it organized all the images and CSS files used for each page. Justine worked on the front-end pertaining to the HTML and CSS side of the project. The most important file would be the app.py, because it has to be run for all the CSS and Python to work on our site. Naomi worked on the back-end pertaining to the SQL, Flask, and Python of the project, as well as some of the front-end HTML code.  

## Acknowledgments
In addition to the libraries and API mentioned above, we also used the following resources:
- flask-app-demo repository by lzblack / Zhi Li on GitHub
- ChatGPT (per professor's suggestion)
- Stack Overflow 
  - https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask
- Geeks for Geeks
  - https://www.geeksforgeeks.org/random-numbers-in-python/
  - https://www.geeksforgeeks.org/get-current-date-using-python/ 

## Reflection 

From the process point of view, some challenges included the length of time spent debugging and trying to figure out how to format the results on the pages. Time for project scoping could have been longer and incorporated into class time to brainstorm together, because it is hard to identify whether a project is doable or too hard in the beginning. As you are running out of time, it could be too late to change the project given the short amount of time you have to work on the project. Testing took the biggest chunk of our time, because there was a lot of debugging and making sure that the CSS was working with flask. Overall, working on it together with the professor to debug was the most effective way to debug and move to the next step, because when the app.py doesn’t work we are unable to run the html page with the CSS as well; Everything is paused to try to debug.  

From a learning perspective, we learned a lot about how to integrate front-end and back-end work using Flask. We will continue to use the formatting needed when integrating CSS and Flask, and ChatGPT. ChatGPT was helpful in generating the newsletter suggestions for each category and for times we needed to debug, but for more specific problems like how to make the dashboard page with each suggestion to be a checkbox we were not able to get a correct answer from ChatGPT. Overall, this project has taught us not only a variety of technical skills, but also soft skills like collaboration, patience, and problem-solving that are very applicable and becoming increasingly demanded in the workplace. 
