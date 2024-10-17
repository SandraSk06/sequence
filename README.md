# sequence web app
Sample WebApp to show messages received from MQTTX server in a sequence.
* Python
* JavaScript
* HTML/CSS
* js-sequence-diagrams library

# References
https://bwmarrin.github.io/MkDocsPlus/js-sequence-diagrams/

## Steps
* Connect and subscribe with MQTTX server using Python and web page is rendered
* On Ok-button click, message having an 'id' and 'msg' fields sent from MQTTX server. This is shown in a table.
* On each table row click, a popup is displayed. Inside the popup a sequence is shown based on 'id'.

## Example
MQTTX server messages:
Topic: testQoS: 0
{
  "id": 4,
  "msg": "1start"
}

Topic: testQoS: 0
{
  "id": 4,
  "msg": "2start"
}

Topic: testQoS: 0
{
  "id": 4,
  "msg": "3start"
}

Topic: testQoS: 0
{
  "id": 4,
  "msg": "end"
}

Sequence
<img width="159" alt="Screenshot 2024-10-17 192739" src="https://github.com/user-attachments/assets/6a321193-de7b-4252-b187-c9377cf5fb37">

