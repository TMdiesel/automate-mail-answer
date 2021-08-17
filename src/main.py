# default package
import datetime
import logging

# third package
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import jpholiday
from selenium.webdriver.support.select import Select

# my package
import mail_utils as mu

logger = logging.getLogger("Log")


def _isBizDay() -> bool:
    """
    今日が休日かどうか判定する
    Return:
        休日:True
        営業日:False
    """
    Date = datetime.datetime.now()
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return True
    else:
        return False


def automate_chrome(URL: str, save_ss: bool = True) -> None:
    """
    seleniumでchromeを操作して回答を登録する

    Args:
        URL (str): 体調確認回答のURL
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    # answer
    # Q1:いいえ
    Select(
        driver.find_element_by_xpath("//select[@name='inputcmb_1']")
    ).select_by_index(1)
    # Q2:いいえ
    Select(
        driver.find_element_by_xpath("//select[@name='inputcmb_2']")
    ).select_by_index(1)
    # Q3:休み or テレワーク
    if _isBizDay():
        Select(
            driver.find_element_by_xpath("//select[@name='inputcmb_3']")
        ).select_by_index(3)
    else:
        Select(
            driver.find_element_by_xpath("//select[@name='inputcmb_3']")
        ).select_by_index(2)
    # Q4:オフィス在籍
    Select(
        driver.find_element_by_xpath("//select[@name='inputcmb_4']")
    ).select_by_index(7)
    # Q5:自宅
    Select(
        driver.find_element_by_xpath("//select[@name='inputcmb_5']")
    ).select_by_index(7)
    logger.info("successfully put your answer")
    if save_ss:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        driver.save_screenshot("./img/answer_%s.png" % (now))
        logger.info("save screenshot of your answer")

    # register
    driver.find_element_by_xpath("//input[@name='btnReg2']").click()
    Alert(driver).accept()
    if save_ss:
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        driver.save_screenshot("./img/register_%s.png" % (now))
        logger.info("save screenshot of your register")
    logger.info("successfully register your answer")
    logger.info("page source")

    driver.quit()


def main() -> None:
    formatter = "%(levelname)s : %(name)s : %(asctime)s : %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)

    msg = mu.get_msg()
    URL = mu.content_to_URL(msg)
    automate_chrome(URL, save_ss=False)


if __name__ == "__main__":
    main()
