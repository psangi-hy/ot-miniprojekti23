*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Select Article

*** Test Cases ***
Add Article And Check That Bibtex Is Correct
    Set Author  Thomas Mitchell
    Set Title  Machine Learning
    Set Journal  Sensors
    Set Year  2018
    Set Volume  18
    Set Pages  26
    Submit Content
    Submit Should Succeed


*** Keywords ***
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

Submit Should Succeed
    Go To Bibtex Page
    Bibtex Page Should Be Open
    Page Should Contain  @article
    Page Should Contain  author = {Thomas Mitchell}
    Page Should Contain  title = {Machine Learning}
    Page Should Contain  journal = {Sensors}
    Page Should Contain  year = {2018}
    Page Should Contain  volume = {18}
    Page Should Contain  pages = {26}