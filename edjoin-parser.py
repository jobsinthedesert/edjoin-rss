import time
import argparse
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin

def open_browser(url):
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(firefox_options=options, executable_path=r'geckodriver')
    browser.get(url)
    time.sleep(3)
    return browser

def open_url(url):
    browser = open_browser(url)
    soup = bs.BeautifulSoup(browser.page_source, 'lxml')
    browser.quit()
    return soup

def check_pagination(soup):
    """
    Determines if there are multiple pages of job listings
    """
    pagination = soup.find('div', {'class': 'pagination'})

    if len(pagination) > 0:
        return True
    else:
        return False

def search_jobs(url):
    """
    Searches for all available jobs
    """
    soup = open_url(url)

    jobs_list = []
    
    for job in jobs(soup):
        jobs_list.append(job)
    
    if check_pagination(soup) == True:
        pagination = soup.find('div', {'class': 'pagination'})
        current_page = 1
        pages = pagination.find_all('li')
        no_pages = len(pages)-2
        print(no_pages)
        page_str_index = url.find('page=')

        while current_page < no_pages:
            next_page_url = url[:page_str_index+5] + str(current_page+1) + url[page_str_index+6:]
            print(current_page)
            new_soup = open_url(next_page_url)
            
            for job in jobs(new_soup):
                jobs_list.append(job)

            current_page += 1

    return jobs_list

def jobs(soup):
    """
    Returns job name and link for table within page
    """
    jobs_table_soup = soup.find('tbody')
    jobs_soup = jobs_table_soup.find_all('tr')

    for job in jobs_soup:
        link = urljoin('https://www.edjoin.org/', job.find('a').get('href'))
        title = job.find('a').text
        yield link, title

def format_element(job, opening_tag, closing_tag):
    """
    Formats <link> and <title> elements
    """
    return('    '+opening_tag+job+closing_tag+'\n')

def format_item(title, link):
    """
    Joins <title> and <link> elements as children of <item>
    """
    return('  <item>\n'+title+link+'  </item>\n')

def sanitize_title(title):
    """
    Alters forbidden chracters in XML
    """
    clean_amp = title.replace('&', '&amp;')
    clean_quot = clean_amp.replace('"', '&quot;')
    clean_apos = clean_quot.replace('\'', '&apos;')
    clean_lt = clean_apos.replace('<', '&lt;')
    clean_gt = clean_lt.replace('>', '&gt;')

    clean_title = clean_gt

    return clean_title

def format_jobs(jobs):
    """
    Concatenates a string to return a list of jobs as <item> elems
    """

    job_item_string = ''

    for job in jobs:
        job_name = sanitize_title(job[1])
        title = format_element(job_name, '<title>', '</title>')
        link = format_element(job[0], '<link>', '</link>')
        item = format_item(title, link)
        job_item_string += item

    return job_item_string

def format_rss(jobs, title, link):
    """
    Returns an RSS feed as a string
    """
    xml_opening = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    rss_opening = '<rss version="2.0">\n\n'
    channel_opening = '<channel>\n'
    
    channel_title = '  <title>'+title+'</title>\n'
    channel_link = '  <link>'+link+'</link>\n'

    header = xml_opening + rss_opening + channel_opening + channel_title + channel_link

    job_items = format_jobs(jobs)

    channel_closing = '</channel>\n'
    rss_closing = '</rss>'

    closing = channel_closing + rss_closing

    rss_feed = header + job_items + closing

    return rss_feed

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-url', required=True, help="edjoin url")
    parser.add_argument('-output', required=True, help="name of rss file ex: feed.xml")
    parser.add_argument('-title', required=True, help="name in RSS feed <title> tag")
    parser.add_argument('-link', required=True, help="location in RSS feed <link> tag")

    args = parser.parse_args()

    jobs = search_jobs(args.url)
    rss_feed = format_rss(jobs, args.title, args.link)

    with open(args.output, 'w+') as f:
        f.write(rss_feed)

if __name__ == '__main__':
    main()
