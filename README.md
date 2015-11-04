#Network communication using email service
For the need of passing data between random PCs,
With or without firewall, other networks etc.  ->  one can use this library


###Configuring Gmail account
- We recomend creating new Gmail account dedicated for project
- Filters
    * Run FilterGenerator.py with all the this-user field's which will use this email
    * add the generated Filters.xml file to:  Settings=>Filters_and_Blocked_Addresses=>Import_filters
- enter the account while your logged ingo to this link and turn it on:
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
- An example of chat(with and without gui) between two PCs included
- for now just ascii text is supported
