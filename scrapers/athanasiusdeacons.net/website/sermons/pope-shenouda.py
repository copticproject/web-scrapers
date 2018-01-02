from lib.webtests import WebTests
from lib.output import Output

output = Output()

with WebTests() as driver:
    driver.go_to('http://www.athanasiusdeacons.net/data/Download.aspx?id=31')

    pages = []
    for link in driver.find_all("//table[@id='ctl00_ContentPlaceHolder1_DataList1']/tbody/tr/td/table/tbody/tr/td[2]/a"):
        pages.append(link.get_attribute('href'))

    for page in pages:
        driver.go_to(page)

        for item in driver.find_all("//table[@id='ctl00_ContentPlaceHolder1_GridView1']/tbody/tr"):
            title = item.find_element_by_xpath("td[1]/table/tbody/tr[1]/td/a").text
            year = item.find_element_by_xpath("td[1]/table/tbody/tr[4]/td/span").text
            link = item.find_element_by_xpath("td[3]/table/tbody/tr/td[1]/a").get_attribute('href')
            print("%s|%s|%s" % (title, year, link))

            output.add('ar', title, page, link, '', 'البابا شنودة', 'audio')

output.write()