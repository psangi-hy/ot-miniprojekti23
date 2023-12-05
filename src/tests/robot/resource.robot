*** Settings ***
Library  SeleniumLibrary
Library  ./AppLibrary.py
Library  RequestsLibrary

*** Variables ***
${SERVER}  localhost:5001
${DELAY}  0.0 seconds
${HOME URL}  http://${SERVER}
${NEW URL}  http://${SERVER}/new
${BIBTEX URL}  http://${SERVER}/bibtex
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
    Title Should Be  New Reference

Bibtex Page Should Be Open
    Title Should Be  BibTeX Entries

Select Article
    Go To New Page
    Click Element  id:referenceType
    Select From List By Value  id:referenceType  article

Go To New Page
    Go To  ${NEW URL}

Go To Front Page
    Go To  ${HOME URL}

Go To Bibtex Page
    Go To  ${BIBTEX URL}
