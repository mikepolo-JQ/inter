from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class MainPage(PageObject):
    h1 = PageElement(By.CSS_SELECTOR, "h1")
    h2 = PageElement(By.CSS_SELECTOR, "h2")
    # p = PageElement(By.CSS_SELECTOR, "p")
    # a = PageElement(By.CSS_SELECTOR, "a")
    # # nav = PageElement(By.CSS_SELECTOR, "nav")
