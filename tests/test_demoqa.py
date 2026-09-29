import pytest
from playwright.sync_api import Page, expect
import time

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

