Download
---------------------
Get the latest script [here](https://raw.github.com/opendns/Deploy-Scripts/master/Labtech/OpenDNS%20Umbrella%20Roaming%20Agent.xml).

Notes
-----

This script deploys the roaming client for **Windows only**.
There is currently no support for any other operating system. 
The script will simply exit if run on OS X or Linux.

The following variables must be set ahead of time:
  * `ORGID_FROM_CONFIG_FILE`
  * `FINGERPRINT_FROM_CONFIG_FILE`
  * `USERID_FROM_CONFIG_FILE`

Their values can be retrieved from the [MSP Console->Roaming Agent->Deploy](https://dashboard2.opendns.com/msp#roamingclient/deploy) page

What the script does
--------------------

1. Make the `%windir%\ltsvc\scripts` folder
2. Download the [Roaming Client msi](http://shared.opendns.com/roaming/enterprise/release/win/production/Setup.msi) to the above folder
3. If the file is unable to be download, open a ticket
4. Use `msiexec` to install the downloaded MSI file silently and with no UI.
5. Open a ticket documentating that the roaming client has been installed.

Warning
--------------------

Renaming the file from Setup.msi or changing the path of the file will likely result in a failed installation. In order for the Roaming Client to function correctly, it must be installed as Setup.msi
