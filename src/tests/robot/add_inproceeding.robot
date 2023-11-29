*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${CONTENT_TYPE}  application/x-www-form-urlencoded

*** Test Cases ***
Add Inproceeding With Required Content Using POST
    Create Session  mysession  ${HOME URL}
    &{headers}=  Create Dictionary  Content-Type=${CONTENT_TYPE}
    &{data}=  Create Dictionary  type=inproceeding  author=Inproceeding Writer  title=Test Inproc.  year=2005  booktitle=Robot Tests
    ${response}=  POST On Session  mysession  /new  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${response.status_code}  200
    POST Submit Inproceeding Should Succeed  Inproceeding Writer  Test Inproc.  2005  Robot Tests

Missing Author Field Using POST
    Create Session  mysession  ${HOME URL}
    &{headers}=  Create Dictionary  Content-Type=${CONTENT_TYPE}
    &{data}=  Create Dictionary  type=inproceeding  author=  title=Fail Inproc.  year=2000  booktitle=Test Booktitle
    ${response}=  POST On Session  mysession  /new  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${response.status_code}  200
    POST Submit Inproceeding Should Fail  ""  Fail Inproc.  2000  Test Booktitle

Missing Title Field Using POST
    Create Session  mysession  ${HOME URL}
    &{headers}=  Create Dictionary  Content-Type=${CONTENT_TYPE}
    &{data}=  Create Dictionary  type=inproceeding  author=Test Writer  title=  year=2000  booktitle=Test Booktitle
    ${response}=  POST On Session  mysession  /new  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${response.status_code}  200
    POST Submit Inproceeding Should Fail  Test Writer  ""  2000  Test Booktitle

Missing Year Field Using POST
    Create Session  mysession  ${HOME URL}
    &{headers}=  Create Dictionary  Content-Type=${CONTENT_TYPE}
    &{data}=  Create Dictionary  type=book  author=Test Writer  title=Fail Inproc.  year=  booktitle=Test Booktitle
    ${response}=  POST On Session  mysession  /new  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${response.status_code}  200
    POST Submit Inproceeding Should Fail  Test Writer  Fail Inproc.  ""  Test Booktitle

*** Keywords ***
POST Submit Inproceeding Should Succeed
    [Arguments]  ${author}  ${title}  ${year}  ${booktitle}
    Go To Front Page
    Page Should Contain  ${author}
    Page Should Contain  ${title}
    Page Should Contain  ${year}
    Page Should Contain  ${booktitle}

POST Submit Inproceeding Should Fail
    [Arguments]  ${author}  ${title}  ${year}  ${booktitle}
    Go To Front Page
    Page Should Not Contain  ${author}
    Page Should Not Contain  ${title}
    Page Should Not Contain  ${year}
    Page Should Not Contain  ${booktitle}