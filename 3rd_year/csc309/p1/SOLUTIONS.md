## Group Members
### Please follow the format-> Student 1: Name of student (Student ID)
- Student 1: Ruoxuan Guo (1002956964)
- Student 2: Jiayu Li (1002206784)
- Student 3: Yichong Guan (1002730529)
- Student 4: Zhihong Wang (1002095207)

## Project Description:
In our project, we will use JavaScript, Google Place API (maybe more APIs during development) and other tools to build
a web application in order to help students in University of Toronto to find restaurants and Food Trucks (Mobile Dinner)
around St. George campus, with their requirements (like price levels, what kind of food, ratings/reviews, etc.).
We may add "Favorite" list for users to save the restaurant they love and more features in the future.

Google Place API qualifies as RESTful.
Reasons:
1. Uniform Interface (which is like Google Map, Google APIs interface for resources inside system which are exposed to API consumers and follow religiously);
2. Client-Server Architectural (client(our) application and Google server application are able to evolve separately without any dependency);
3. Statelessness (session states all contains by client, Google server will not store anything about latest HTTP request client made. It will treat each and every request as new);
4. Cacheability (caching shall be applied on resources when applicable, which can be implemented on Google server or client (our) side);
5. Layered system (client(we) cannot ordinarily tell whether it is connected directly to the end server, or to an intermediary along the way);
6. Coding on demand (Client-side scripting).

Three functions:
1. getListOfItems:
Get the restaurant list of nearby restaurants with a particular range by Google Place API.
You can know that we chose restaurants in Sydney by checking "place" and "restaurant" above.

2. getOneItemById: (Id can defined by ourselves)
Get one restaurant by ID.

3. getOneAttributeFromItem:
Get "geometry" attribute from ID 1 restaurant.