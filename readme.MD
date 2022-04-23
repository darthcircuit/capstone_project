# **Info Oxen - Competency Tracker**
## John Ipson
### *Capstone Project*
---
&nbsp;
&nbsp;
&nbsp;

## **Launching the Program**

The program can be started by running:

```
pipenv -install
pipenv shell
python main.py
```

&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;

This will take you to a login window:


You can log into your account using your automatically generated email and password.

To get started, you can log in with:

```
harv.s@infoxen.com
missingsockfinder
```

&nbsp;
&nbsp;
&nbsp;

```
Welcome Stranger! Please Log in!
Please type in your Email Address (or leave blank to quit): harv.p@infoxen.com
Please Type in your password: *********
```
&nbsp;
&nbsp;
&nbsp;

```

Your account has been disabled. Please speak with your manager. 


 User Choice  | First Name  | Last Name   | Email Address          |
 1            | Perkin      | Dene        | perkin.d@infoxen.com   |
 2            | Candice     | Durbyn      | candice.d@infoxen.com  |
 3            | Cointon     | Eastwell    | cointon.e@infoxen.com  |
 4            | Jason       | Fletcher    | jason.f@infoxen.com    |
 5            | John        | Ipson       | john.i@infoxen.com     |
 6            | Maggi       | MacBrearty  | maggi.m@infoxen.com    |
 7            | Christi     | Morgen      | christi.m@infoxen.com  |




Please type in your Email Address (or leave blank to quit): 

```

&nbsp;
&nbsp;
&nbsp;

**OH NO!** Poor Harv's Account has been disabled!

&nbsp;
&nbsp;
&nbsp;

Before we fix it, let's log in with:

```
ben.n@infoxen.com
fedexguyimpersonator
```

&nbsp;
&nbsp;
&nbsp;


##
## Employee's Menu

### Ben's Account will take you to the Employee Portal.


&nbsp;
&nbsp;
&nbsp;

```
Welcome back Ben Nicklaus!
You last logged in on 2022-04-23


!!WARNING!!

      - There were 1 failed login attempts to your account since your last successful Login!




      [1]: Change your password
      [2]: View your assessment results and passed competencies
      [3]: Log Out


Please select an option: 
```
&nbsp;

Employees have very limited access to the system. They are only allowed to update their password, and view their own progress.

In this view, we can also see if there was a failed login attempt to your account.

Following the Menu prompts will let you either change your password, view your progress or log out of the system.

&nbsp;

```
:View your Competency Progress:
 Competency  | Competecy ID  | Employee Name  | Email  | assess_id  | average_score  |



      [1]: Change your password
      [2]: View your assessment results and passed competencies
      [3]: Log Out


Please select an option: 2

```


&nbsp;

It doesnt look like Ben has completed any assesments yet, so let's log out and we'll take a look at the Manager's Portal.

&nbsp;

## Manager's Menu
Use this account:


```
jason.f@infoxen.com
bandaidsupplyofficer
```

This will give you access to the Manager's portal where you can make changes system wide.

```
Welcome back Jason Fletcher!
You last logged in on Never
You are logged in with Admin Privelages. Please be careful as you edit data.


      [1]: Change your password
      [2]: Change another User's Password
      [3]: View Users, Competencies, and Assessments
      [4]: Add Users or Competencies/Assessments
      [5]: Edit User Information, Competencies, and Assessments
      [6]: View your Competency Progress
      [7]: View, Add and Edit Assessment Results
      [8]: Import and Export Reports
      [9]: Log Out


Please select an option: 

```

Most of the options are fairly self explainatory, but we'll go over some of them more in depth.

&nbsp;

Select Option 2, and we can search for Harv's account. Before we reactivate his account, we should probably reset his password. Go ahead and choose something you like. But it has to be funny, or else you have to do it again.


&nbsp;

If we select option 3, we can view a list of every User, Competency and Assessment in our Database.

```
:View Users, Competencies,and Assessments:


      [1]: Users
      [2]: Competencies
      [3]: Assessments
      [4]: Go Back
```
You're in for a real treat when you run one of those reports.

&nbsp;

Back at the main menu, if we select Option 4, we are given the opportunity to create a new user or competency. We do not need to create assessments manually, as they are automatically created for you whenever you create or edit a competency. You will be given a list of information desired when creating that will help the system.

When creating a user, Email Addresses and Passwords are automatically generated. You can either change this info before you give it to your employees or you can let them update the password themselves.

&nbsp;

Option 5 lets you edit existing information.

When you want to edit or update a user, you have the option of searching by the first or last name of the employee. You can also just press enter to view everyone at once. 

From here, let's find Harv's account again. You will be able to set his "status" to '1' which will make his account active again, meaning he can once again log in.

Harv has been doing a great job at the company lately, so we're also going to set him up as a Manager. Let's follow the same procedure to edit his account and change the 'user_type' to '1'. Users with a type 0 are regular employees. Type 1 users are managers. They probably had to do one of those color tests.
```
:Edit User Information, Competencies, and Assessments:
Assessments are automatically updated when a competency is edited.


      [1]: Edit User
      [2]: Edit Competency
      [3]: Go Back


Please Select an option: 1


Please Type a User's name to search, or leave blank to view all users: harv
```
```

user_id        1
first_name     Harv
last_name      Stoodale
email          harv.s@infoxen.com
password       $2b$12$3.oQylSOr.iqDCNCLMQEku37EihDfCrE9Nw221TqLo2rpRw5B.PwO
last_login     2022-01-24
failed_logins  8
date_created   2021-02-17
date_hired     2021-04-15
user_type      1
status         1



Please select one of the following options, or press enter to cancel: 
1) first_name: 
2) last_name: 
3) email: 
4) password: 
5) date_hired: 
6) user_type: 
7) status: 
```

&nbsp;

When you make a change you'll be able to see that get reflected in the table above the menu.

&nbsp;

There is no need for a search function for competencies at this time, but as the amount of data tracking we do grows, this feature could be implemented if there was enough call for it. When you edit a competency, however, the associated Assessments are also updated to reflect the changes you made.

&nbsp;

Back at the menu again, let's look at Options 7 and 8:

```
      [7]: View, Add and Edit Assessment Results
      [8]: Import and Export Reports
```

&nbsp;


Option 7 gives us the option of manually entering Scores, Viewing employee results on an individual basis, or by a single competency. If you need to update the score of an assesment, you can see a list of all the results for every competency and user.

You are also given the option to delete a result if it is getting in the way. Sometimes I wish I could delete things that got in my way in real life.

```
      [1]: View Results for an Individual
      [2]: View All Results for a Competency
      [3]: Enter Results for an Individual
      [4]: Edit Results for an Assesment
      [5]: Delete an Assessment Result
      [6]: Go Back
```

&nbsp;

*Report for individual user*
```
 Competency        | Competecy ID  | Employee Name  | Email               | assess_id  | average_score  |
 Computer Anatomy  | 1             | Ipson, John    | john.i@infoxen.com  | 1.1        | 3.0            |
 Recursion         | 15            | Ipson, John    | john.i@infoxen.com  | 15.1       | 3.0            |
```

&nbsp;

&nbsp;
*Selecting a Competency, and then reporting all scores for it*
```

 Competency ID  | Name                         | Date Created  |
 1              | Computer Anatomy             | 2022-01-03    |
 2              | Data Types                   | 2022-01-07    |
 3              | Variables                    | 2022-02-13    |
 4              | Functions                    | 2022-02-21    |
 5              | Boolean Logic                | 2022-04-02    |
 6              | Conditionals                 | 2022-04-04    |
 7              | Loops                        | 2022-03-02    |
 8              | Data Structures              | 2022-04-11    |
 9              | Lists                        | 2022-04-13    |
 10             | Dictionaries                 | 2022-03-17    |
 11             | Working With Files           | 2022-02-28    |
 12             | Exception Handling           | 2022-03-15    |
 13             | Quality Assurance (QA)       | 2022-04-08    |
 14             | Object-Oriented Programming  | 2022-03-14    |
 15             | Recursion                    | 2022-02-08    |
 16             | Databases                    | 2022-04-19    |
 17             | Toenail Collecting           | 2022-04-22    |
 18             | Nosehair Inspecting          | 2022-04-22    |

Enter the Competency ID that you would like to view a report of: 1
 Competency        | Competecy ID  | Employee Name  | Email               | assess_id  | average_score  |
 Computer Anatomy  | 1             | Ipson, John    | john.i@infoxen.com  | 1.1        | 3.0            |

      [1]: View Results for an Individual
      [2]: View All Results for a Competency
      [3]: Enter Results for an Individual
      [4]: Edit Results for an Assesment
      [5]: Delete an Assessment Result
      [6]: Go Back


Please Select an option: 2

```


&nbsp;

*Viewing all recorded Assessment Results and selecting one to correct the score*
```
 Choice  | Last Name  | First Name  | Assessment Name                        | Result ID  | Attempt Score  |
 1       | Ipson      | John        | Recursion - Manager Evaluation         | 15.1.2.1   | 3              |
 2       | Ipson      | John        | Recursion - Peer Evaluation            | 15.2.2.1   | 4              |
 3       | Ipson      | John        | Recursion - Practical Skills           | 15.3.2.1   | 3              |
 4       | Ipson      | John        | Recursion - Self Evaluation            | 15.4.2.1   | 2              |
 5       | Ipson      | John        | Computer Anatomy - Manager Evaluation  | 1.1.2.1    | 3              |
 6       | Ipson      | John        | Computer Anatomy - Peer Evaluation     | 1.2.2.1    | 2              |
 7       | Ipson      | John        | Computer Anatomy - Practical Skills    | 1.3.2.1    | 3              |
 8       | Ipson      | John        | Computer Anatomy - Self Evaluation     | 1.4.2.1    | 3              |
 9       | Ipson      | John        | Recursion - Manager Evaluation         | 15.1.2.2   | 3              |
 10      | Ipson      | John        | Recursion - Peer Evaluation            | 15.2.2.2   | 4              |
 11      | Ipson      | John        | Recursion - Practical Skills           | 15.3.2.2   | 3              |
 12      | Ipson      | John        | Recursion - Self Evaluation            | 15.4.2.2   | 2              |
 13      | Ipson      | John        | Computer Anatomy - Manager Evaluation  | 1.1.2.2    | 3              |
 14      | Ipson      | John        | Computer Anatomy - Peer Evaluation     | 1.2.2.2    | 4              |
 15      | Ipson      | John        | Computer Anatomy - Practical Skills    | 1.3.2.2    | 4              |
 16      | Ipson      | John        | Recursion - Manager Evaluation         | 15.1.2.3   | 3              |
 17      | Ipson      | John        | Recursion - Peer Evaluation            | 15.2.2.3   | 4              |
 18      | Ipson      | John        | Recursion - Practical Skills           | 15.3.2.3   | 3              |
 19      | Ipson      | John        | Recursion - Self Evaluation            | 15.4.2.3   | 2              |
 20      | Ipson      | John        | Computer Anatomy - Manager Evaluation  | 1.1.2.3    | 3              |
 21      | Ipson      | John        | Computer Anatomy - Peer Evaluation     | 1.2.2.3    | 2              |
 22      | Ipson      | John        | Computer Anatomy - Practical Skills    | 1.3.2.3    | 3              |
 23      | Ipson      | John        | Computer Anatomy - Self Evaluation     | 1.4.2.2    | 3              |

Enter the choice that you would like: 
```


&nbsp;

If we go back to the main menu and select Option 8, we will get into arguably the most important part of the tool.

Option 8 allows you to import and export CSV files to help you import assessment data faster as well managing it in bulk. You can also perform more powerful reports from your favorite dedicated spreadsheet application. Pop your export into Lotus 123, and baby you've got a stew going.

&nbsp;

*Here is where the real power of the competency tracker comes into play.*
```
:Import and Export Reports:
      [1]: Export Individual User Assessment Report to CSV
      [2]: Export Competency Assessment Report to CSV
      [3]: Import CSV with Assessment Result information
      [4]: Generate template for importing scores from CSV
      [5]: Go Back
```


&nbsp;

This menu will save you a considerable amount of time when entering scores. From here, you can generate a template file to help you get the correct formatting for import.


&nbsp;

All the files for import or export will be available in the Reports folder in the main application directory.

If you would like to see how each part of the database relates to each other, I've included a PDF of the Database Schema. That file is in the main folder of the program and is called ERD.pdf.

If any of the operations in this program were unclear, please don't hesitate to reach out to me.