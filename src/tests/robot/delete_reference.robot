*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${REFTITLE}  Proximate composition of Vitex doniana and Saba comorensis fruits
${REFAUTHOR}  Charles, Dominic and Mgina, Clarence
${REFJOURNAL}  Scientific Reports
${REFYEAR}  2023

*** Test Cases ***
Deleting A Reference Removes It From The Front Page
	Create Reference
	Reference Should Exist On The Front Page
	Delete Reference
	Reference Should Not Exist On The Front Page

*** Keywords ***
Create Reference
	Select Article
	Input Text  author  ${REFAUTHOR}
	Input Text  title  ${REFTITLE}
	Input Text  journal  ${REFJOURNAL}
	Input Text  year  ${REFYEAR}
	Click Button  Save

Reference Should Exist On The Front Page
	Go To Front Page
	Page Should Contain  ${REFTITLE}
	
Delete Reference
	Go To Reference Page  ${REFTITLE}
	Click Button  Delete reference

Reference Should Not Exist On The Front Page
	Go To Front Page
	Page Should Not Contain  ${REFTITLE}
	
Go To Reference Page
	Go To Front Page
	[Arguments]  ${name}
	Click Element  partial link:${name}
	
