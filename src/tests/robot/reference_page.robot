*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${REFTITLE}  Proximate composition of Vitex doniana and Saba comorensis fruits
${REFAUTHOR}  Charles, Dominic and Mgina, Clarence
${REFJOURNAL}  Scientific Reports
${REFYEAR}  2023
${REFVOLUME}  13
${REFPAGES}  14--15

*** Test Cases ***
The Reference Page Contains Information About The Reference
	Create Reference
	Go To Reference Page  ${REFTITLE}
	Page Should Contain  ${REFTITLE}
	Page Should Contain  ${REFAUTHOR}
	Page Should Contain  ${REFJOURNAL}
	Page Should Contain  ${REFYEAR}
	Page Should Contain  ${REFVOLUME}
	Page Should Contain  ${REFPAGES}

*** Keywords ***
Create Reference
	Select Article
	Input Text  author  ${REFAUTHOR}
	Input Text  title  ${REFTITLE}
	Input Text  journal  ${REFJOURNAL}
	Input Text  year  ${REFYEAR}
	Input Text  volume  ${REFVOLUME}
	Input Text  pages  ${REFPAGES}
	Click Button  Save
