## Welcome to "Address Database":
The Project creates a Graphical User Interface to *Store*, *Retrieve* and *Maintain8 addresses in a Database.  
Login feature is added so that only specific people can access the addresses.  
There is also an ADMIN which manages all the users and makes sure who gets the access.  
The passwords are encrypted to ensure security and in case of forgetting passwords,   
it can be retrieved by the users through email.

### Python Libraries Used:
* **tkinter:** To create the Graphical User Interface.  
* **sqlite3:** For the Database functionality.  
* **cryptography:** To Encrypt the Passwords.
* **smtplib:** To send Emails in case of forget password.
* **os**, **pathlib** and **dotenv**: For accessing the .env file.

---
### Login Window:
This Window allows a User to Login after they have provided their  
correct Username and Password. If Wrong credentials are provided  
then an Error Message will be displayed

![Login Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Login.png)

**SignUp Button:** This button opens up *"The SignUp Window"*.  
**Forgot Password:** Clicking here opens up *"The Forgot Password Window"*.

---
### SignUp Window:
This Window allows a New User to create an account by providing  
their details and *The Secret Key*. The Secret Key is given by the Admin  
so that not anyone can come and make account and access anything.

If Incorrect Secret Key is provided then an Error message will be displayed.

![SignUp Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/SignUp.png)

**Submit Button:** After filling the details clicking here will create your account.  
**Back Button:** Clicking here will allow us to go back to *"Login Window"*.

---
### Forgot Password Window:
In this Window we need to provide our Email_ID, using which we created  
our account, and our Password will be sent to that Email_ID.

If Incorrect Email_ID is provided then an Error Message is displayed.

![Forgot Password Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Forgot_Password.png)

**Send Button:** After providing the Email_ID, clicking will send our password to our Email_ID.  
**Back Button:** Clicking here will allow us to go back to *"Login Window"*

---
### Home Window:
This Window allows us to access the Address Database to insert, search, update and delete records.  
We also have access to File Menu, Settings Menu and Admin Settings(Only for Admin).

Below we have the Status Bar displaying the current User.

![Home Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Home.png)

**Insert Button:** Opens the *"Insert Window"* and gives access to Inserting in the Addresses Table.  
**Search Button:** Opens the *"Search Window"* and gives access to Searching in the Addresses Table.
**Update Button:** Opens the *"Update Window"* and gives access to Updating in the Addresses Table.
**Delete Button:** Opens the *"Delete Window"* and gives access to Deleting in the Addresses Table.  

**File Menu:**
* Insert: Same as **Insert Button**.
* Search: Same as **Search Button**.
* Update: Same as **Update Button**.
* Delete: Same as **Delete Button**.
* Logout: Closes *"Home Window"* and opens *"Login Window"*.
* Exit: Closes the Program.

**Setting Menu:**
* User Details: Opens the *"User Details Window"*.
* Change Password: Opens the *"Change Password Window"*.

**Admin Settings Menu:**
* All User Details: Opens the *"All User Details Window"*.
* Change Secret Key: Opens the *"Change Secret Key Window"*.

---
### User Details Window:
This Window displays the details of the Current User and allows  
the User to change the details. 

![User Details Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/User_Details.png)

**Change Button:** Allows the User to edit his/her details.  
**Save Button:** Allows the User to Save the changes made.  
**Back Button:** Takes the User back to *"Home Window"*.

---
### Change Password Window:
This Window allows the User to change his/her Password.  
The User needs to first provide the Current Password, then  
type in the New Password and finally Confirm the New Password.

An Error Message will be displayed if the User does not type  
the correct Current Password or the New Password and Confirm   
Password does not match.

![Change Password Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Change_Password.png)

**Save Button:** Changes the User's Password  
**Back Button:** Takes the User back to *"Home Window"*.

---
### All User Details Window:
This Window is accessible only to the Admin and here the Admin  
can see the details of all the Users having account.

![All User Details Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/All_User_Details.png)

**Remove Button:** After selecting a particular User, allows the Admin to remove that particular User.  
**Back Button:** Takes the User back to *"Home Window"*.

---
### Change Secret Key Window:
This Window is accessible only to the Admin.  
It allows the Admin to change his/her Password.  
The User needs to first provide the Current Secret Key, then  
type in the New Secret key and finally Confirm the New Secret Key.

An Error Message will be displayed if the Admin does not type  
the correct Current Secret Key or the New Secret Key and Confirm   
Secret Key does not match.

![Change Secret Key Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Change_Secret_Key.png)

**Forgot Secret key Button:** Opens the *"Forgot Secret Key Window"*  
**Save Button:** Changes the Secret Key  
**Back Button:** Takes the User back to *"Home Window"*.

---
### Forgot Secret Key Window:
In this Window Admin needs to provide his/her Email_ID, using which he/she   
created his/her account, and the Secret Key will be sent to that Email_ID.

If Incorrect Email_ID is provided then an Error Message is displayed.

![Forgot Secret Key Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Forgot_Secret_Key.png)

**Send Button:** After providing the Email_ID, clicking will send the Secret Key to Admins Email_ID.  
**Back Button:** Clicking here will allow us to go back to *"Change Secret Key Window"*

---
### Insert Window:
This Window lets us Insert Data into the **Addresses** Table.  
The User fill in the details and click the submit button to  
add the record inside the table.

![Insert Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Insert.png)

**Submit Button:** Inserts the Data filled into the **Addresses** Table.  
**Back Button:** Takes the User back to *"Home Window"*.

---
### Search Window:
This Window allows the User to search for a particular Address.  
We have to first select the *Search by* option, then type the  
search value and finally click on the *Search Button* to display  
searched Address record or records.

We can also display everything inside the **Addresses** Table by Clicking  
the *Show All Button*.

![Search Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Search.png)

**Search Button:** Allows us to make searches based on our search value.  
**Show All Button:** Displays every record in **Addresses** Table.
**Back Button:** Takes the User back to *"Home Window"*.

---
### Update Window:
This Window allows the User to Update a record in the **Addresses** Table.  
We first type in the OID of the record which we are interested in  
updating, then we press the *Show Button* to display the details.

Now we can update the record by editing the Entry Fields.   
Finally, pressing the *Update Button* will update the record.

![Update Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Update.png)

**Show Button:** Displays the record details for the corresponding OID value provided.  
**Update Button:** Updates the record.   
**Back Button:** Takes the User back to *"Home Window"*.

---
### Delete Window:
This Window allows the User to Delete a record in the **Addresses** Table.  
The User provides the OID value for the record to be Deleted and  
pressing the *Delete Button* deletes the record.

![Delete Window](https://raw.githubusercontent.com/debroglie27/AddressDatabase/main/UI_Images/Delete.png)

**Delete Button:** Deletes the record for which OID was provided.  
**Back Button:** Takes the User back to *"Home Window"*.

---
## THE END 
### Thank You for reading through The Project.