# linkedin_scraper


1. DESCRIPTION

The package is built to scrape the alumni webpage of each college on LinkedIn (for example, https://www.linkedin.com/school/georgia-institute-of-technology/people/). It can also extract the insights data from the webpages, including where you live, where they work, what they do, what they studied and what they are skilled at. 

The list of colleges in United States comes from College Scoreboard by US Department of Education. You can download it at https://collegescorecard.ed.gov/data/ or access it by its API. Once you have the college list, you can create corresponding Linkedin urls from the names. The step can be done in Excel easily but the urls should be validated before throwing it into the program. The file data/linkedin_schools_demo.csv shows some expected examples.

Besides, due to the policy of LinkedIn, the package cannot guarantee that it can work smoothly for every account. But generally, each account can scrape 200~300 webpages until reaching the searching limit. You need to change another valid account or wait for a new calendar month to reset the limit.


2. INSTALLATION

First of all, the project was written in Python 3.7.

You can install necessary packages in the requirements.txt. If you have pip installed, you can run the following code in the terminal:

    pip install -r requirements.txt
    
The program uses Selenium and Chrome to accomplish the scraping. So you should have the ChromeDriver downloaded and added to the environment path. Follow the official documentation from Selenium (https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) to finish the setup.


3. EXECUTION

The data folder contains some files for demo use. Fill in the username and password of your LinkedIn account in linkedin_scraping.py. To execute the program, run the command "python linkedin_scraping.py" in the terminal and it will scrape two colleges for demonstration.

To extract data from webpages, run the extract_page.py to get nested data in json format and flattened data in csv format.
