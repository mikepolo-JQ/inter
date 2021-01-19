import pytest

from tests.functional.pages import MainPage
from tests.functional.utils import screenshot_on_failure

url = "http://localhost:8000"


@pytest.mark.functional
@screenshot_on_failure
def test(browser, request):
    page = MainPage(browser, url)

    validate_title(page)
    validate_content(page)


def validate_title(page: MainPage):
    assert "mikepolo site" in page.title


def validate_content(page: MainPage):
    assert page.h1.tag_name == "h1"
    assert page.h1.text == "MIKEPOLO SITE"
    assert page.h2.tag_name == "h2"
    assert page.h2.text == "Welcome to"

    # assert page.a.tag_name == "a"
    # assert page.a.text == "ABOUT"
    # assert page.a.tag_name == "a"
    # assert page.a.text == "SERVICE"
    # assert page.a.tag_name == "a"
    # assert page.a.text == "WORK"
    # assert page.a.tag_name == "a"
    # assert page.a.text == "BLOCK"
    # assert page.a.tag_name == "a"
    # assert page.a.text == "CONTACT"
    #
    # assert page.a.tag_name == "a"
    # assert page.a.text == "Learn More"

    # html = page.html
    # assert "<hr>" in html
