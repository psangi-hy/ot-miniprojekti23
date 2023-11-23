*** Settings ***
Library  SeleniumLibrary
Library  ./AppLibrary.py

*** Variables ***
${SERVER}  localhost:5001
${DELAY}  0.0 seconds
${HOME URL}  http://${SERVER}
${NEW URL}  http://${SERVER}/new


*** Keywords ***
Open And Configure Browser
    # jos käytät Firefoxia ja Geckodriveriä käytä seuraavaa riviä sitä alemman sijaan
    #${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
    ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    Call Method    ${options}    add_argument    --no-sandbox
    # seuraava rivi on kommentoitu pois tässä vaiheessa
    Call Method  ${options}  add_argument  --headless
    Open Browser  browser=chrome  options=${options}
    Set Selenium Speed  ${DELAY}

Front Page Should Be Open
    Title Should Be  Articles

Go To New Page
    Go To  ${NEW URL}