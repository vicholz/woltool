# woltools

Tool to poll Google Sheet for machines to send WOL requests to.

## Installation

```bash
mkdir -p ~/git
cd ~/git
git clone https://github.com/vicholz/woltool
cd ~/git/woltool
vi woltool.service # Replace ${GSHEET_URL} with Google Sheet/Script Application URL (EXAMPLE: https://script.google.com/macros/s/LONG_HASH/exec)
sudo cp woltool.service /etc/systemd/system/woltool.service
systemctl daemon-reload
systemctl start woltool
```
