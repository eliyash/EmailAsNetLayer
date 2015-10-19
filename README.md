#Network communication using email service
For the need of passing data between random PCs,
With or without firewall, other networks etc.  ->  one can use this library


###Configuring Gmail account
- Make a Gmail account dedicated for this
- Make a label in the same name as the "this-user" field in the json file will have
- Make a filter which forwardes emails addressed youremail+this-user@gmail.com to this-user label
- Allow the use of untrusted apps:
    * while in your account go to this link and turn it on
    * https://www.google.com/settings/security/lesssecureapps


###Configuring the app
- copy the file called "prog_data_example.json" to prog_data.json and update its data


####Notes & Work in progress
- For now we are relaying on gmail service
- There is just two PCs communication so far
- You have a different script for sending and receiving massages
- Add option of fetching all the received massages
