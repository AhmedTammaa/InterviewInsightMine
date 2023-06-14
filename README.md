# Interview Inshight Mine

This projects aims at collecting and analyzing interview questions from Glassdoor.
The project is currently on it's first phase, it is focused on data-oriented roles.
* Data Science (Main focus)
* Data Analysis 
* Data Engineering

## Progress until now
All of data science interviews from FAANG is scraped and saved into csv files.

## Libraries and tools
* Python 3.10.1
* Selenium
* Beautiful Soup
* Plotly (for Visualization)
* Jupyter notebook
## Usage
1. Go to the company you want to scrape its interview
2. Filter the job interview
3. Get the paged link (e.g. go to page 2, then change the IP2 in the link to IP1)
4. Plug the link into the ```config.py``` 
5. Fill the rest of the data into the ```config.py``` 
6. Run the scraper script ```$ Python scraper.py```
7. Wait for it until it finishes scrapping
8. Run the ```data_cleaner.ipynb``` 
9. Get your final csv file it will be named ```items_$company_name.csv```
10. Enjoy analyzing your data (this repo will contain data analysis in the future)
## Future Plans (for now)
The project is still on scarping phase, so far, 9000+ data science interviews.
There will be a data analysis scripts and insights for the collected data. 
## Contact
If you have any inquires or need anything relevant to the project feel free to email me.
