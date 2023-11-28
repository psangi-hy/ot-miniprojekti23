*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To New Page

*** Test Cases ***
Add Book With Required Content
    Set Key  Testi00
    Set Author  Book Writer
    Set Title  Test Book
    Set Year  1986
    Submit Content
    Submit Should Succeed  Book Writer  Test Book  

*** Keywords ***
Submit Should Succeed
    [Arguments]  ${author}  ${title}  ${year}
    Front Page Should Be Open
    Page Should Contain  ${author}
    Page Should Contain  ${title}
    Page Should Contain  ${year}

Submit Should Fail
    [Arguments]  ${argument}
    Page Should Not Contain  BibTeX Format
    Go To Front Page
    Page Should Not Contain  ${argument}

Set Key
    [Arguments]  ${key}
    Input Text  key  ${key}

Set Author
    [Arguments]  ${author}
    Input Text  author  ${author}

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}
    
Set Journal
    [Arguments]  ${journal}
    Input Text  journal  ${journal}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}

Set Volume
    [Arguments]  ${volume}
    Input Text  volume  ${volume}

Set Pages
    [Arguments]  ${pages}
    Input Text  pages  ${pages}

Submit Content
    Click Button  Save