*** Settings ***
Library  SeleniumLibrary
Library  ./AppLibrary.py

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0.0 seconds
${HOME URL}  http://${SERVER}
${NEW URL}  http://${SERVER}/new


*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Set Selenium Speed  ${DELAY}

Front Page Should Be Open
    Title Should Be  Articles

Go To New Page
    Go To  ${NEW URL}