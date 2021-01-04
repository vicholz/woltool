# woltools

Tool to poll Google Sheet for machines to send WOL requests to.

## Google Sheet Installation
1. Create a new Google Sheet and name it something appropriate like WakieWakie.
1. Rename the sheet to WOL.
1. For the first row enter the following names: Host, MAC, Wake, Last Status.
1. For the second and following rows add a Host, MAC, FALSE.
1. Change the Wake column to TRUE for host you want to send WOL packets to.
1. Open the 'Script Editor' (Tools>Script Editor).
1. Copy the contents of [woltool.gs](https://raw.githubusercontent.com/vicholz/woltool/master/woltool.gs).
1. Paste and replace the contents of the Code.gs file in the 'Script Editor'.
1. Save.
1. Click Deploy>New Deployment in the upper right of the 'Script Editor'.
1. Click on the gear next to 'Select Type' and click 'Web App'.
1. Enter the following:
  Descrition: woltool (or anything you want)
  Execute as: Me
  Who has access: Anyone
1. Click 'Deploy'.
1. Authorize access and follow prompts to allow app. Once complete you will be presented with an ID and a URL. Copy and save this URL somewhere in your Google Sheet for to make it easier to find. (EXAMPLE URL: https://script.google.com/macros/s/LONG_HASH/exec).

## Server Installation

```bash
mkdir -p ~/git
cd ~/git
git clone https://github.com/vicholz/woltool
cd ~/git/woltool
vi woltool.service # Replace ${GSHEET_URL} with Google Sheet/Script Application URL (EXAMPLE URL: https://script.google.com/macros/s/LONG_HASH/exec)
sudo cp woltool.service /etc/systemd/system/woltool.service
sudo systemctl daemon-reload
sudo systemctl start woltool
sudo systemctl status woltool
```
