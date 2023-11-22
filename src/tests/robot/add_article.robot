*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To New Page

*** Test Cases ***
Add Article With All Content
    Set Key  Testi04
    Set Author  Test Author
    Set Title  Great Article
    Set Journal  Testi
    Set Year  2020
    Set Volume  4
    Set Pages  54-60
    Submit Content
    Submit Should Succeed  Testi04

*** Keywords ***
Submit Should Succeed
    [Arguments]  ${key}
    Front Page Should Be Open
    Page Should Contain  ${key}

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