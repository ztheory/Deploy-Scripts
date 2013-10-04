Current versions do not support deploying to Mac OS X.


The unpacked versions of these script were generated using the LabTechXML.py script and are here for descriptive/educational purposes only, you should not attempt to import them into LabTech.

Description/output of visual
1	Note: ***** If not a Windows OS, Exit Script	Exit On Failure	Non Windows OS
2	Exit Script	Exit On Failure	Non Windows OS
3	   SHELL:  mkdir %windir%\ltsvc\scripts and store the result in %shellresult%	Continue On Failure	All Operating Systems
4	   DOWNLOAD:  http://shared.opendns.com/roaming/enterprise/release/win/production/Setup.msi  saved to  %windir%\ltsvc\scripts\Setup.msi  and wait until finish.	Continue On Failure	All Operating Systems
5	   IF FILE Exists  %windir%\ltsvc\scripts\Setup.msi  THEN  Jump to :InstallFixIt	Exit On Failure	All Operating Systems
6	   LOG:  %windir%\ltsvc\scripts\Setup.msi failed to download. Exiting script...	Exit On Failure	All Operating Systems
7	   Create New Ticket for %clientid%\%computerid% Email:%ContactEmail% Subject:Umbrella Roaming Client Failed to install on %ComputerName%. #FAILURE	Exit On Failure	All Operating Systems
8	Exit Script	Exit On Failure	All Operating Systems
9	:InstallFixIt - Label	Exit On Failure	All Operating Systems
10	   SHELL:  msiexec /i %windir%\ltsvc\scripts\Setup.msi /qn ORG_ID=@ORGID_FROM_CONFIG_FILE@ ORG_FINGERPRINT=@FINGERPRINT_FROM_CONFIG_FILE@ USER_ID=@USERID_FROM_CONFIG_FILE@ HIDE_UI=1 HIDE_ARP=1 and store the result in %shellresult%	Continue On Failure	All Operating Systems
11	   LOG:  OpenDNS Agent has been installed.	Exit On Failure	All Operating Systems
12	   Create New Ticket for %clientid%\%computerid% Email:%ContactEmail% Subject:Umbrella Roaming Client COMPLETED on %ComputerName% #SUCCESS	Exit On Failure	All Operating Systems
