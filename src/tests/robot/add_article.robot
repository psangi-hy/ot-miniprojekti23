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
    Submit Should Succeed  Test Author  Great Article  Testi  2020

Empty Author Field
    Set Key  Testi01
    Set Title  Robot Testing
    Set Journal  Computers
    Set Year  2013
    Submit Content
    Submit Should Fail  Robot Testing

Empty Title Field
    Set Key  Testi02
    Set Author  Test Author
    Set Journal  Computers
    Set Year  2013
    Submit Content
    Submit Should Fail  2013

Empty Journal Field
    Set Key  Testi03
    Set Author  Test Author
    Set Title  Robot Testing
    Set Year  2013
    Submit Content
    Submit Should Fail  Robot Testing

Empty Year Field
    Set Key  Testi04
    Set Author  Test Author
    Set Title  Robot Testing
    Set Journal  Computers
    Submit Content
    Submit Should Fail  Computers


*** Keywords ***
Submit Should Succeed
    [Arguments]  ${author}  ${title}  ${journal}  ${year}
    Front Page Should Be Open
    Page Should Contain  ${author}
    Page Should Contain  ${title}
    Page Should Contain  ${journal}
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