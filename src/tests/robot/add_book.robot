*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${CONTENT_TYPE}  application/x-www-form-urlencoded

*** Test Cases ***
Add Book With Required Content Using POST
    Create Session  mysession  ${HOME URL}
    &{headers}=  Create Dictionary  Content-Type=${CONTENT_TYPE}
    &{data}=  Create Dictionary  type=book  author=Book Writer  title=Test Book  publisher=Publishing House  year=1986
    ${response}=  POST On Session  mysession  /new  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${response.status_code}  200
    POST Submit Book Should Succeed  Book Writer  Test Book  1986  Publishing House

*** Keywords ***
POST Submit Book Should Succeed
    [Arguments]  ${author}  ${title}  ${year}  ${publisher}
    Go To Front Page
    Page Should Contain  ${author}
    Page Should Contain  ${title}
    Page Should Contain  ${year}
	Page Should Contain  ${publisher}
