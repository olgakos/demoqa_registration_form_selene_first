from selene.support.shared import browser
from pathlib import Path
from selene import have, be
from selene import command
import os
import tests
from tests import resources

def test_student_registration_form():
    #Open
    browser.open('/automation-practice-form')
    browser.element('.practice-form-wrapper').should(have.text('Student Registration Form'))

    #AdBlockers
    browser.all('[id^=google_ads][id$=container__]').with_(timeout=2).wait_until(
        have.size_greater_than_or_equal(3)
    )
    browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)
    #browser.element('footer').execute_script('element.remove()')

    # WHEN
    browser.element('#firstName').type('Olga')
    browser.element('#lastName').type('Kos')
    browser.element('#userEmail').type('kos@example.com')
    browser.all('[name=gender]').element_by(have.value('Female')).element('..').click()
    browser.element('#userNumber').type('0123456789')

    #Calendar
    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__month-select').type('April')
    browser.element('.react-datepicker__year-select').type('1995')
    browser.element(
        f'.react-datepicker__day--0{23}:not(.react-datepicker__day--outside-month)'
    ).click()

    #Subjects
    browser.element('#subjectsInput').type('Computer Science').press_enter()

    #Hobbies
    browser.all('.custom-checkbox').element_by(have.exact_text('Reading')).click() #best practice
    #browser.element('[for=hobbies-checkbox-2]').click() #Reading

    #Photo
    browser.element('#uploadPicture').set_value(
        os.path.abspath(os.path.join(os.path.dirname(tests.__file__), 'resources/foto.jpg')
        )
    )
    #browser.element('#uploadPicture').send_keys(os.getcwd() + '/foto2.jpg') #only if the photo is in the same folder as the test

    #Current Address
    browser.element('#currentAddress').type('Moscowskaya Street 16')

    #State and City
    browser.element('#state').perform(command.js.scroll_into_view) #!
    browser.element('#state').click()
    browser.all('[id^=react-select][id*=option]').element_by(
        have.exact_text('NCR')
    ).click()

    browser.element('#city').click()
    browser.all('[id^=react-select][id*=option]').element_by(
        have.exact_text('Delhi')
    ).click()

    #or:
    # browser.execute_script("window.scrollBy(0, 500)")
    # browser.element('#react-select-3-input').should(be.blank).type('NCR').press_enter()
    # browser.element('#react-select-4-input').should(be.blank).type('Delhi').press_enter()

    #Submit Button
    browser.element('#submit').perform(command.js.click)

    # THEN
    browser.element('.table').all('td').even.should(
        have.exact_texts(
        'Olga Kos',
        'kos@example.com',
        'Female',
        '0123456789',
        '23 April,1995',
        'Computer Science',
        'Reading',
        'foto.jpg',
        'Moscowskaya Street 16',
        'NCR Delhi',
        )
    )