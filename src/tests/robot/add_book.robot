*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To New Page

*** Test Cases ***
Add Book With Required Content
    Set Author  Book Writer
    Set Title  Test Book
    Set Year  1986
    Submit Content
    Submit Should Succeed  Book Writer  Test Book  

Empty Author
    Set Title  Empty Book
    Set Year  1986
    Submit Content
    Submit Should Fail  Empty Book

Empty Title
    Set Author  Test Writer
    Set Year  2011
    Submit Content
    Submit Should Fail  Test Writer

Empty Year
    Set Author  Test Writer
    Set Title  Empty Book
    Submit Content
    Submit Should Fail  Empty Book

*** Keywords ***
Submit Should Succeed
    [Arguments]  ${author}  ${title}  ${year}
    Front Page Should Be Open
    Page Should Contain  ${author}
    Page Should Contain  ${title}
    Page Should Contain  ${year}

Submit Should Fail
    [Arguments]  ${parameter}
    Page Should Not Contain  BibTeX Format
    Go To Front Page
    Page Should Not Contain  ${parameter}

Set Key
    [Arguments]  ${key}
    Input Text  key  ${key}

Set Author
    [Arguments]  ${author}
    Input Text  author  ${author}

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}

Set Publisher
    [Arguments]  ${publisher}
    Input Text  publisher  ${publisher}

Set Volume
    [Arguments]  ${volume}
    Input Text  volume  ${volume}

Set Pages
    [Arguments]  ${pages}
    Input Text  pages  ${pages}

Submit Content
    Click Button  Save