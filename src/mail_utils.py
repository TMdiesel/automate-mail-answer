# default package
import imaplib
import email
import re
import os
import logging
import datetime


logger = logging.getLogger("Log").getChild("sub")


def get_msg() -> "msg":
    """
    IMAP serverからGmailの受信メールを取得

    Returns:
        msg
    """
    UserName = os.environ.get("UserName", "")
    PassName = os.environ.get("PassName", "")
    CompanyEmail = os.environ.get("CompanyEmail", "")

    gmail = imaplib.IMAP4_SSL("imap.gmail.com", "993")
    gmail.login(UserName, PassName)
    gmail.select()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        "%d-%b-%Y"
    )
    search_option = '(FROM "%s" SENTSINCE "%s")' % (CompanyEmail, yesterday)

    try:
        typ, data = gmail.search(None, search_option)
        logger.info("succesfully get message from gmail")
    except Exception as e:
        logger.error(e)

    for num in data[0].decode().split():
        typ, data = gmail.fetch(num, "(RFC822)")
        msg = email.message_from_string(data[0][1].decode())

    gmail.close()
    gmail.logout()

    return msg


def _get_content(msg) -> str:
    """
    msgからメール本文を取得する

    Args:
        msg
    Returns:
        str: メール本文
    """
    charset = msg.get_content_charset()
    payload = msg.get_payload(decode=True)
    try:
        if payload:
            if charset:
                return payload.decode(charset)
            else:
                return payload.decode()
        else:
            return ""
    except Exception as e:
        logger.error(e)
        return payload  # デコードできない場合は生データにフォールバック


def content_to_URL(msg) -> str:
    """
    メール本文からURLを取り出す
    Args:
        msg
    Returns:
        URL
    """
    content = _get_content(msg)
    content_list = re.split("[\r|\n]", content)
    URL = [content for content in content_list if content.startswith("http")][0]
    logger.info(URL)

    return URL


if __name__ == "__main__":
    """
    test
    """
    msg = get_msg()
    URL = content_to_URL(msg)
    print(URL)
