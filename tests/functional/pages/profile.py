from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject


class ProfilePage(PageObject):
    needed_help_info = PageElement(By.CSS_SELECTOR, "#id_profile_needed_help")
    provide_help_info = PageElement(By.CSS_SELECTOR, "#id_profile_provide_help")

    needed_input = PageElement(By.CSS_SELECTOR, "#input_need_help")
    provide_input = PageElement(By.CSS_SELECTOR, "#input_provide_help")
    edit_button = PageElement(By.CSS_SELECTOR, "#id_edit_button")
    update_profile_button = PageElement(By.CSS_SELECTOR, "#id_profile_update_button")
    start_button = PageElement(By.CSS_SELECTOR, "#id_profile_smart_start")
