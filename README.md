# edjoin-rss

EDJOIN, "the number one education job site", is regularly adding new job postings. Some school districts and organizations see plenty of positions being added while others are updated less frequently.  Are you tired of refreshing a school district's job listings every day only to find out that nothing has changed?  Well, edjoin-rss aims to automate the process of checking for new job postings.

edjoin-rss is a Python script that will parse job listings within a school district and create an RSS feed which contains the job title and a link to the description for each job found.

### How does edjoin-rss alert me when a new job is posted?

It doesn't.  At least not by itself.  The ideal scenario is to set the script to run daily and then use 'git status' to check if any changes have been made to a feed.

## Usage

    edjoin-parser.py -u "school district url" -o "output_file.xml" -t "user created feed title" -l "user created link" 

Example:

    edjoin-parser.py -u "https://www.edjoin.org/Home/Jobs?rows=10&page=1&sort=postingDate&order=desc&keywords=&searchType=&states=&regions=&jobTypes=&days=0&catID=0&onlineApps=false&recruitmentCenterID=0&stateID=0&regionID=0&districtID=565&countyID=0&searchID=0" -o "../jobsinthedesert-feeds/desert_sands_usd.xml" -t "Desert Sands Unified School District Careers | Jobs in the Desert"  -l "https://jobsinthedesert.github.io/jobs/education/desert_sands_usd/"
    
## Built With

* Python 3
  * bs4
  * lxml
  * selenium
* geckodriver
