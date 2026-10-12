import pytest
from pytest_check import check
from playwright.sync_api import Page, expect
import time
from datetime import date
from faker import Faker 
import random

fake = Faker('en_US')

@pytest.mark.skip
def test_some_entities(page):
    page.goto('https://demoqa.com')
    time.sleep(10)


def test_text_box(page: Page):
    page.goto('https://demoqa.com/text-box', wait_until='domcontentloaded')
    time.sleep(1) 

    username_locator = '#userName'
    page.type(username_locator, 'John Doe')
    time.sleep(1)
    
    email_locator = '#userEmail'
    page.type(email_locator, 'john.doe@email.com')
    time.sleep(1)
    
    address_locator = '#currentAddress'
    page.type(address_locator, 'WD17 4BQ, Watford')
    time.sleep(1)

    page.click('#submit')
    time.sleep(1)  

    expect(page.locator('#output #name')).to_have_text('Name:John Doe')
    expect(page.locator('#output #email')).to_have_text('Email:john.doe@email.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :WD17 4BQ, Watford')

    time.sleep(1)

def test_button_demoqa(page: Page):
    page.goto('https://demoqa.com/webtables', wait_until='domcontentloaded')
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Registration Form")).to_be_visible(visible=True)
    page.get_by_placeholder("First Name").type(fake.first_name(), delay=50)
    page.get_by_placeholder("Last Name").type(fake.last_name(), delay=50)
    page.get_by_placeholder("name@example.com").type(fake.email(), delay=50)
    page.get_by_placeholder("Age").type(str(random.randint(15, 25)), delay=50)
    page.get_by_placeholder("Salary").type(str(random.randint(50, 3000)), delay=50)
    page.get_by_placeholder("Department").type("IT", delay=50)
    
    page.get_by_role("button", name="Submit").click()
    time.sleep(1)
    expect(page.get_by_role("button", name="Submit")).not_to_be_visible()
    time.sleep(1)

def test_form_demoqa(page: Page):
    
    today_date = date.today().strftime("%d %b %Y")
    print(f"Today's date: {today_date}")

    page.goto('https://demoqa.com/automation-practice-form', wait_until='domcontentloaded')
    
    page.get_by_placeholder("First Name").type(fake.first_name(), delay=50)
    page.get_by_placeholder("Last Name").type(fake.last_name(), delay=50)
    page.get_by_placeholder("name@example.com").type(fake.email(), delay=50)

    page.check(f'#gender-radio-{random.randint(1, 3)}')

    page.get_by_placeholder("Mobile Number").type(fake.numerify("##########"), delay=50)
    
    subjects_field = page.locator('#subjectsInput')
    subjects_field.type("Maths", delay=50)
    subjects_field.press("Enter")

    page.check(f'#hobbies-checkbox-{random.randint(1, 3)}')

    page.get_by_placeholder("Current Address").type(fake.street_address(), delay=50)

    # сверка даты
    current_date_value = page.get_attribute('#dateOfBirthInput', 'value')
    print(f'Current date from page: {current_date_value}')
    check.is_equal(current_date_value, today_date, "dates not equal")

    # выбор штата
    page.locator('#state').click()

    state_listbox = page.locator('#react-select-3-listbox')

    expect(state_listbox).to_be_visible()
    state_options = state_listbox.get_by_role("option")
    state_count = state_options.count()

    print(f"State кол-во опций: {state_count}")

    page.locator(f'#react-select-3-option-{random.randint(0, 2)}').click()
    time.sleep(1)

    # выбор города
    page.locator('#city').click()
    city_listbox = page.locator(f'#react-select-4-listbox')

    expect(city_listbox).to_be_visible()
    city_options = city_listbox.get_by_role("option")
    city_count = city_options.count() - 1

    print(f"City кол-во опций: {city_count}")

    page.locator(f'#react-select-4-option-{random.randint(0, city_count)}').click()

    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Thanks for submitting the form")).to_be_visible()
    expect(page.get_by_role("button", name="Close")).to_be_visible()

    time.sleep(3)


def test_check_forms(page: Page):

    page.goto('https://demoqa.com/radio-button', wait_until='domcontentloaded')

    yesradio = page.is_enabled('#yesRadio')
    impressiveradio = page.is_enabled('#impressiveRadio')
    noradio = page.is_enabled('#noRadio')

    check.is_true(yesradio, "yesradio isn't active")
    check.is_true(impressiveradio, "impressiveradio isn't active")
    check.is_false(noradio, "noradio shouldn't be active")
    
    time.sleep(2)

def test_check_visibility(page: Page):
    
    page.goto("https://demoqa.com/checkbox")

    expect(page.get_by_role("checkbox", name="Select Home")).to_be_visible()
    expect(page.get_by_role("checkbox", name="Select Desktop")).not_to_be_visible()

    page.locator(".rc-tree-switcher").click()
    
    expect(page.get_by_role("checkbox", name="Select Desktop")).to_be_visible()

def test_wait_for_selector(page: Page):

    page.goto("https://demoqa.com/dynamic-properties")

    page.get_by_role("button", name="Visible After 5 Seconds").wait_for(state='visible')

    expect(page.get_by_role("button", name="Visible After 5 Seconds")).to_be_visible()
