## TO-DO in this file

- Include names of your team members
- Explain the features of your web application, the end-user and how s/he might use it.
- A note if you plan on submitting the assignment late.

- Student 1: Ruoxuan Guo (1002956964)
- Student 2: Jiayu Li (1002206784)
- Student 3: Yichong Guan (1002730529)
- Student 4: Zhihong Wang (1002095207)

Explanation:

In our assignment 2, we used HTML, CSS(3), jQuery, JavaScript and Google Place API for web development. The goal of our
A2 project is to help students at the University of Toronto to find nearby restaurants around St. George campus.

As users, when they open our website, there will be a welcome view (First View) show up. This view contains a background
image and a clickable button "Go Find Food".

If the user clicks that button, it will lead him/her to our main application view (Second View), also called the "Find
Food" view, with 3 buttons at the top. In this view, users can select a campus building from existing building list.
The default setting of the building is "Bahen Centre (BA)". After choosing a building, users may choose a number of meters
as the radius of restaurant search area. The default radius is 200 meters. Then, they can click "click to see restaurants
round" button. This button will change the content in scrollable "result" block by adding all restaurants in the distance
bound around the selected building. These restaurants show as clickable buttons in "result". In the same time, at the right
side of our second view, the Google Map will display all restaurants in "result". Users can simply click one of them, then
it will link to the official Google Map. Users may choose one of the restaurants in "result", then they can see the detail
information of that restaurant (if that restaurant does not have any information in Google Map API, then our website will
tell the user "No Detail Information"). This action will also change the "Restaurant Name" (the "header" of CSS div "card")
at the third view and recenter the map to the restaurant chosen by the user.

To go to the "Comment" view (Third View), users can click the "comment" button at the top. These top buttons are existing
in all views except the first welcome view, which let users make comments or find restaurants anytime as long as they
remain on this website. At the right side of "Comment" view, there is a "Comment Here!" block. Users are able to write
comments for the restaurant they chose at "Find Food" view. After the user finishes commenting and click "Submit" button,
the right side of "Comment" view will record these comments in the "container" of "card".

Because A2 requirements, we should not store any data of the user, so we do not create login view. All modifications in
the Google Map, "result" of the second view and "card" of the third view that produced by users will not be recorded in
A2 (i.e. If user refreshes the whole page, everything will be reinitialized).

Due to lack of back-end, we do not have the database to map building names to specific latitude and longitude, so we have
to hard-coding the LatLng data for four buildings. This is only for demonstration of this function, we will fully implement
this function in assignment 3 to let users select any building inside UofT campus.