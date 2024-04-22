import csv
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Initialize the Chrome driver with options
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920x1080")
# service = Service('C:\\Users\\anafl\\OneDrive\\Documentos\\poc-ao3\\chromedriver.exe')
service = Service('C:\\Users\\umaanaflavia\\OneDrive\\Documentos\\poc-ao3\\chromedriver.exe')
driver = webdriver.Chrome(options=options, service=service)


url1 = "https://archiveofourown.org/works/search?commit=Search&work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=&work_search%5Blanguage_id%5D="
url2 = "&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=_score&work_search%5Bsort_direction%5D=desc"
languages = ['es','ru','zh']

link_list = []
arquivos = []

for l in languages:
    link_list.append(url1+l+url2)
    arquivos.append(l+'.csv')


driver.get(link_list[0])
time.sleep(3)
button = driver.find_element(By.ID, "tos_agree")
button.click()
time.sleep(1)
button = driver.find_element(By.ID, "accept_tos")
button.click()

for index in range(len(link_list)):
    driver.get(link_list[index])

    # Create and open a CSV file for writing information
    with open(arquivos[index], 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = ['id',
                   'title',
                   'authors',
                   'fandoms',
                   'rating',
                   'warnings',
                   'category',
                   'completion',
                   'date',
                   'relationships',
                   'characters',
                   'freeforms',
                   'summary',
                   'language',
                   'words',
                   'chapters',
                   'comments',
                   'kudos',
                   'bookmarks',
                   'hits']
        csv_writer.writerow(headers)
        print(languages[index])

    while True:
        print(driver.current_url)
        elements = driver.find_elements(By.CSS_SELECTOR, '[id^="work_"]')
        for element in elements:
            # Heading
            link_element = element.find_element(By.CLASS_NAME, 'heading')            
            title_element = link_element.find_element(By.TAG_NAME, 'a')
            href = title_element.get_attribute('href')
            work_id = re.search(r'/works/(\d+)', href).group(1)
            title = title_element.text
            try:
                authors = link_element.find_elements(By.TAG_NAME, 'a')[1].text
            except IndexError:
                authors = "Anonymous"

            # Fandoms
            fandoms_element = element.find_element(By.CLASS_NAME, 'fandoms')
            fandoms_tags = fandoms_element.find_elements(By.TAG_NAME, 'a')
            fandoms = []
            for fandom_tag in fandoms_tags:
                fandom = fandom_tag.text.strip()
                fandoms.append(fandom)

            # Required Tags
            required_tags_element = element.find_element(By.CLASS_NAME, 'required-tags')
            required_tags = required_tags_element.find_elements(By.TAG_NAME, 'li')
            rating = required_tags[0].text
            warnings = required_tags[1].text
            category = required_tags[2].text
            completion = required_tags[3].text

            # Date
            date = element.find_element(By.CLASS_NAME, 'datetime').text

            # Tags
            tags_element = element.find_element(By.CLASS_NAME, 'tags')
            
            relationships_element = tags_element.find_elements(By.CLASS_NAME, 'relationships')
            relationships = []
            for relationship_element in relationships_element:
                relationship = relationship_element.text
                relationships.append(relationship)
            
            characters_element = tags_element.find_elements(By.CLASS_NAME, 'characters')
            characters = []
            for character_element in characters_element:
                character = character_element.text
                characters.append(character)
            
            freeforms_element = tags_element.find_elements(By.CLASS_NAME, 'freeforms')
            freeforms = []
            for freeform_element in freeforms_element:
                freeform = freeform_element.text
                freeforms.append(freeform)

            # Summary
            try:
                summary = element.find_element(By.CSS_SELECTOR, 'blockquote.summary').text.replace('\n', ' ')
            except NoSuchElementException:
                summary = ""

            # Stats
            stats_element = element.find_element(By.CLASS_NAME, 'stats')
            language = element.find_element(By.CSS_SELECTOR, 'dd.language').text
            words = element.find_element(By.CSS_SELECTOR, 'dd.words').text
            chapters = element.find_element(By.CSS_SELECTOR, 'dd.chapters').text
            hits = element.find_element(By.CSS_SELECTOR, 'dd.hits').text
            
            try:
                comments = element.find_element(By.CSS_SELECTOR, 'dd.comments').text
            except NoSuchElementException:
                comments = ""
            
            try:
                kudos = element.find_element(By.CSS_SELECTOR, 'dd.kudos').text
            except NoSuchElementException:
                kudos = ""
            
            try:
                bookmarks = element.find_element(By.CSS_SELECTOR, 'dd.bookmarks').text
            except NoSuchElementException:
                bookmarks = ""
            
            # Add line
            with open(arquivos[index], 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                row = [str(work_id),
                    str(title),
                    str(authors),
                    str(fandoms),
                    str(rating),
                    str(warnings),
                    str(category),
                    str(completion),
                    str(date),
                    str(relationships),
                    str(characters),
                    str(freeforms),
                    str(summary),
                    str(language),
                    str(words),
                    str(chapters),
                    str(comments),
                    str(kudos),
                    str(bookmarks),
                    str(hits)]
                csv_writer.writerow(row)

        # Check if there is a "Próxima página" button
        try:
            next_page_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Next →")
            next_page_button.click()
        except NoSuchElementException: # NoSuchElementException is lauched if the element is not foud i.e. if  there's no next page
            break

driver.quit()

