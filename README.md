#Network communication using email service
For the need of passing data between random PCs,
With or without firewall, other networks etc.  ->  one can use this library


###Configuring Gmail account
- Make a Gmail account dedicated for this
- Make a labels called <user> and \<user\>\_received, will \<user\> is same as this-user field in the json file
- Filters
    * Run FilterGenerator.py with all the \<user\>'s which will use this machine
    * add the generated Filters.xml file to:  Settings->Filters_and_Blocked_Addresses->Import_filters
- Allow the use of untrusted apps:
    * while in your account go to this link and turn it on
    * https://www.google.com/settings/security/lesssecureapps


###Configuring the app
- rename the file called "prog_data_example.json" to prog_data.json and update its data
  * email - your gmail account (just the user name - prefix of the email)
  * password - gmails password
  * this user - a name which will be used as your machine name
  * other email - can be same as your email
  * other user 0 - name of the other machine

####Notes & Work in progress
- For now we are relaying on gmail service
- Add option of fetching all the received massages
- An example of chat between two PCs included
