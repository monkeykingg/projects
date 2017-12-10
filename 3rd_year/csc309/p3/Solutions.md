## TO-DO in this file

- Include names of your team members
- Explain the features of your web application, the end-user and how s/he might use it.
- A note if you plan on submitting the assignment late.

- Student 1: Ruoxuan Guo (1002956964)
- Student 2: Jiayu Li (1002206784)
- Student 3: Yichong Guan (1002730529)
- Student 4: Zhihong Wang (1002095207)

Explanation and Instruction:

In our assignment 3, we used ejs, MongoDB, Bootstrap, node.js, express, HTML, CSS, jQuery, AJAX, JavaScript and Google
Place/Map API for web development. The goal of our A3 project is to build a login website for helping students at the
University of Toronto SG to find nearby restaurants around the building they choose and save those favourite restaurants
they like.

As users, when they open our website, there will be a "Login" page show up. If the user registered before, he/she can
simply enter his/her username and password to visit the "Main" page. If there is a new user, he/she can start by click
"Register" link and simply set up username and password to create a new account. Then back to login page and re-login.
If a user tries to login/register with an empty username/password or there already exist the same username in our database,
this action will lead the user to a "Failed" page that shows why the user fails to login/register.

After a successful login, users will see a one-page main view -- our "Main" page. This page contains multiple functions for users.

First, users can see a white search input box at the top-left block, which allows users to enter the two capital letters
building CODE (like BA for Bahen Centre). We also considered those users who do not know what is the building CODE by
providing the selectable list of all buildings in UofT SG campus. The default setting of the building list is "AB -
Astronomy and Astrophysics". Then, users are able to choose their distance bound -- the number of meters as the radius
of restaurant search area. The default radius is 200 meters.

After all selections, they may click "Search Restaurants Around!" button. This button will change the content in scrollable
"Search Result" block by changing "Search Result" text to "Restaurants around XX" (XX refer to what building you typed or
selected) and add all restaurants in the distance bound around the selected building. These restaurants show as clickable
buttons in "Result" block.

If users click one of these "Result Restaurant Buttons", the top-right "Restaurant Info and Comments" block will response.
The "Restaurant Info" header will change to the detail of the restaurant clicked with a "Add to Favourite" button and
"Google Map Page" link; the "Others' Comments from Google" container will get the comment of this restaurant from Google
API. If that restaurant does not have any information on Google Map API, our website will tell the user "No Detail Information".
At the same time, the "Google Map" block will also display all restaurant markers (only if the restaurant has location
information from Google API) refer to "Result". Users can simply click one of them, then it will also show a link to the
official Google Map page.

Now, users may click the "Add to Favourite" button, which is a start point of more back-end and database functions.

Click the "Add to Favourite" button, there will be a "Create" page shows up. This page aims to help users add the restaurant
to their favourite list with a reasonable note. Then, after typed notes and clicked submit, the "Favourite" Page will be
created. In this page, users can find all restaurants they liked before with restaurant names and notes. We also provide
"Delete" and "Edit" buttons for users. "Delete" is simply remove the selected restaurant from favourite list; "Edit" button
works like "Add to Favourite" button which means it will also take users to an "Edit" page (looks like "Create" page) that
let users edit their notes for chosen restaurant and update the old note by click "Submit" button. Users can click "Back
to Main Page" button after they think they manipulate enough. By the way, if users forget to type notes or edit notes to
blank (i.e. the input of notes is empty), then we will direct users to a new "Fail" page and tell them the input should
not be empty. And as the instruction at "Favourite" Page, we recommend users only favourite one restaurant once.

After click "Back to Main Page" button, users will back to "Main" page. Users can see their favourite restaurants again;
log out this website; contact with us by click buttons located at the very top-left corner.