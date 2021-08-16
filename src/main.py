#%%
#default package
import datetime
import time
import logging
#third package
from selenium import webdriver
from selenium.webdriver.common.by import By
import schedule
from selenium.webdriver.common.alert import Alert
import jpholiday
#my package
import mail_utils as mu

formatter = '%(levelname)s : %(name)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='./log/logger.log',level=logging.INFO,format=formatter)
logger = logging.getLogger("Log")

def _isBizDay()->bool:
    """
    今日が休日かどうか判定する
    Return:
        休日:True
        営業日:False
    """
    Date=datetime.datetime.now()
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return True
    else:
        return False

def automate_chrome(URL:str,save_ss:bool=True)->None:
    """
    seleniumでchromeを操作して回答を登録する

    Args:
        URL (str): 体調確認回答のURL
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #options.add_argument('--log-level=3')

    driver = webdriver.Chrome("./driver/chromedriver.exe",options=options)
    driver.get(URL)
    
    try:
        #answer
        driver.find_element_by_xpath("//select[@name='inputcmb_1']/option[2]").click()  #Q1:いいえ
        driver.find_element_by_xpath("//select[@name='inputcmb_2']/option[2]").click()  #Q2:いいえ
        driver.find_element_by_xpath("//select[@name='inputcmb_4']/option[8]").click()  #Q4:オフィス在籍
        driver.find_element_by_xpath("//select[@name='inputcmb_5']/option[8]").click()  #Q5:自宅(テレワーク・休み等)
        if _isBizDay():
            driver.find_element_by_xpath("//select[@name='inputcmb_3']/option[4]").click()  #Q3:休み
        else:
            driver.find_element_by_xpath("//select[@name='inputcmb_3']/option[3]").click()  #Q3:テレワーク
        if save_ss:
            now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') 
            driver.save_screenshot("./png/answer_%s.png"%(now))
            logger.info('save screenshot of your answer')

        #register
        driver.find_element_by_xpath("//input[@name='btnReg2']").click()
        Alert(driver).accept()
        if save_ss:
            now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') 
            driver.save_screenshot("./png/register_%s.png"%(now))
            logger.info('save screenshot of your register')
        logger.info('register your answer')
    except Exception as e:
        logger.error(e)

    driver.quit()

def main()->None:
    msg=mu.get_msg()
    URL=mu.content_to_URL(msg)
    automate_chrome(URL)

#%%
if __name__=='__main__':
    main()


