from selenium.webdriver import Chrome
import pandas as pd
driver = Chrome('C:/users/user/chromedriver/chromedriver.exe')


for i in range(1,10000000):
	u = f"https://www.startupwala.com/list-of-registered-companies-in-india-P{str(i)}"
	driver.get(u)

	urls = driver.find_elements_by_xpath("//td[@class='companyName']/a")  
	urls = [a.get_attribute('href') for a in urls]
	ad = [] 
	for url in urls:
	    driver.get(url)
	    fdata = dict()
	    kpis = ['Company Name','CIN','ROC Name','Date of Incorporation','Registered Address','Authorised Capital','Paid Up Capital','Date of Last AGM','Date of Latest Balance Sheet','Company Status']
	    for kpi in kpis:
	    	fdata[kpi] = driver.find_element_by_xpath(f"//td[contains(text(),'{kpi}')]/parent::tr/td[2]").text.strip()
	    print(fdata)
	    ad.append(fdata)

	    df = pd.DataFrame(ad)
	    df.to_csv('India.csv')

	
	