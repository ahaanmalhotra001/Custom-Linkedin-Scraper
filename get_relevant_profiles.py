import csv
import parameters
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(parameters.driver_loc)
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(2)

driver.find_element_by_xpath('//a[text()="Sign in"]').click()
sleep(3)

username_input = driver.find_element_by_name('session_key')
username_input.send_keys(parameters.username)
sleep(0.5)

password_input = driver.find_element_by_name('session_password')
password_input.send_keys(parameters.password)
sleep(0.5)

# click on the sign in button
driver.find_element_by_xpath('//button[text()="Sign in"]').click()
sleep(3)

driver.get('https://www.google.com/')
sleep(3)

search_input = driver.find_element_by_name('q')
search_query = input('Please Enter the Search Query\n')
place = input('Location\n')

writer = csv.writer(open(search_query + "-" + place + "-Data" +'.csv', 'w', encoding='utf-8'))
writer.writerow(['Name', 'Job Title', 'Location', 'Schools', 'Linkedin Url'])

search_query = 'site: linkedin.com/in/ AND ' + '"' + search_query + '" AND "' + place +'"'
search_input.send_keys(search_query)
sleep(1)

search_input.send_keys(Keys.RETURN)
sleep(3)

profiles = driver.find_elements_by_xpath('//*[@class="g"]/*/*/*/a[1]')
profiles = [profile.get_attribute('href') for profile in profiles]

for profile in profiles:
    driver.get(profile)
    sleep(2)

    sel = Selector(text = driver.page_source)
    name = sel.xpath('//h1/text()').extract_first()
    name = name.strip()
    if 'Jobs' in name:
        continue
    job_title = sel.xpath('//main//section//div/h1/../following-sibling::div[1]/text()').extract_first()
    if job_title :
        job_title = job_title.strip()
    schools = sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract()
    location = sel.xpath('//*[@class="text-body-small inline t-black--light break-words"]/text()').extract_first().strip()
    ln_url = driver.current_url
    writer.writerow([name, job_title, location, schools, ln_url])
    
    try:
        driver.find_element_by_xpath('//*[text()="More"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[text()="Connect"]').click()
        sleep(1)

        try:
            driver.find_element_by_xpath('//*[text()="Connect"]').click()
        except:
            pass
        driver.find_element_by_xpath('//*[text()="Send"]').click()
    except:
        driver.find_element_by_xpath('//*[text()="Connect"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[text()="Send Now"]').click()

driver.quit()


