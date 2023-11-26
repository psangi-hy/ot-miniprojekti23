*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To New Page

*** Test Cases ***
Add Article With All Content
    Set Key  Testi00
    Set Author  Test Author
    Set Title  Great Article
    Set Journal  Testi
    Set Year  2020
    Set Volume  4
    Set Pages  54-60
    Submit Content
    Submit Should Succeed  Testi00

Empty Author Field
    Set Key  Testi01
    Set Title  Robot Testing
    Set Journal  Computers
    Set Year  2013
    Submit Content
    Submit Should Fail  Testi01

Empty Title Field
    Set Key  Testi02
    Set Author  Test Author
    Set Journal  Computers
    Set Year  2013
    Submit Content
    Submit Should Fail  Testi02

Empty Journal Field
    Set Key  Testi03
    Set Author  Test Author
    Set Title  Robot Testing
    Set Year  2013
    Submit Content
    Submit Should Fail  Testi03

Empty Year Field
    Set Key  Testi04
    Set Author  Test Author
    Set Title  Robot Testing
    Set Journal  Computers
    Submit Content
    Submit Should Fail  Testi04


*** Keywords ***
Submit Should Succeed
    [Arguments]  ${key}
    Front Page Should Be Open
    Page Should Contain  ${key}

Submit Should Fail
    [Arguments]  ${key}
    Page Should Contain  New Article
    Go To Front Page
    Page Should Not Contain  ${key}


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