*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Select Article

*** Test Cases ***
Add Article With All Content
    Set Author  Test Author
    Set Title  Great Article
    Set Journal  Testi
    Set Year  2020
    Set Volume  4
    Set Pages  54-60
    Submit Content
    Submit Should Succeed  Great Article  Test Author  2020

Empty Author Field
    Set Title  Robot Testing
    Set Journal  Computers
    Set Year  2013
    Submit Content
    Submit Should Fail  Robot Testing

Empty Title Field
    Set Author  Test Author
    Set Journal  Computers
    Set Year  2013
    Submit Content
    Submit Should Fail  2013

Empty Journal Field
    Set Author  Test Author
    Set Title  Robot Testing
    Set Year  2013
    Submit Content
    Submit Should Fail  Robot Testing

Empty Year Field
    Set Author  Test Author
    Set Title  Robot Testing
    Set Journal  Computers
    Submit Content
    Submit Should Fail  Computers


*** Keywords ***
Submit Should Succeed
    [Arguments]  ${author}  ${title}  ${year}
    Go To Front Page
    Page Should Contain  ${title}
    Page Should Contain  ${author}
    Page Should Contain  ${year}

Submit Should Fail
    [Arguments]  ${argument}
    Page Should Not Contain  BibTeX Format
    Go To Front Page
    Page Should Not Contain  ${argument}

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