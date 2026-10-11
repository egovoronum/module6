import pytest
from playwright.sync_api import Page, expect
import time
from faker import Faker 
import random

fake = Faker()

@pytest.mark.skip
def test_some_entities(page):
    page.goto('https://demoqa.com')
    time.sleep(10)


def test_text_box(page: Page):
    page.goto('https://demoqa.com/text-box', wait_until='domcontentloaded')
    time.sleep(1) 

    username_locator = '#userName'
    page.fill(username_locator, 'John Doe')
    time.sleep(1)
    
    email_locator = '#userEmail'
    page.fill(email_locator, 'john.doe@email.com')
    time.sleep(1)
    
    address_locator = '#currentAddress'
    page.fill(address_locator, 'WD17 4BQ, Watford')
    time.sleep(1)
    
    page.click('#submit')
    time.sleep(1)  

    expect(page.locator('#output #name')).to_have_text('Name:John Doe')
    expect(page.locator('#output #email')).to_have_text('Email:john.doe@email.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :WD17 4BQ, Watford')
    
    time.sleep(1)

def test_button_demoqa(page: Page):
    page.goto('https://demoqa.com/webtables', wait_until='domcontentloaded')
    time.sleep(1)
    page.get_by_role("button", name="Add").click()
    time.sleep(1)
    expect(page.get_by_text("Registration Form")).to_be_visible(visible=True)
    time.sleep(1)
    page.get_by_placeholder("First Name").fill(fake.first_name())
    page.get_by_placeholder("Last Name").fill(fake.last_name())
    page.get_by_placeholder("name@example.com").fill(fake.email())
    page.get_by_placeholder("Age").fill(str(random.randint(15, 25)))
    page.get_by_placeholder("Salary").fill(str(random.randint(1000, 3000)))
    page.get_by_placeholder("Department").fill("IT")
    page.get_by_role("button", name="Submit").click()
    time.sleep(3)
