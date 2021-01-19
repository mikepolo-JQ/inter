import pytest

from tests.functional.pages.hello import HelloPage
from tests.functional.utils import screenshot_on_failure
from tests.functional.utils import validate_redirect

url = "http://localhost:8000/hello/"


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request):
    page = HelloPage(browser, url)

    assert page.greeting.text == "Hello, Anon!"
    assert page.address.text == "Your location is XZ."

    page.name_input.clear()
    page.address_input.clear()
    page.name_input.send_keys("Mike")
    page.submit_button.click()
    validate_redirect(page, url)
    assert page.greeting.text == "Hello, Mike!"
    assert page.address.text == "Your location is XZ."
    # assert page.name_input.get_attribute("value") == "Mike"

    page.name_input.clear()
    page.address_input.clear()
    page.address_input.send_keys("localhost")
    page.submit_button.click()
    validate_redirect(page, url)
    assert page.greeting.text == "Hello, Anon!"
    assert page.address.text == "Your location is localhost."
    # assert page.address_input.get_attribute("value") == "localhost"

    page.name_input.clear()
    page.address_input.clear()
    page.name_input.send_keys("Mike")
    page.address_input.send_keys("localhost")
    page.submit_button.click()
    validate_redirect(page, url)
    assert page.greeting.text == "Hello, Mike!"
    assert page.address.text == "Your location is localhost."
    # assert page.name_input.get_attribute("value") == "Mike"
    # assert page.address_input.get_attribute("value") == "localhost"
