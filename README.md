# full_stack_python_javascript

Set up
-start django project music_controller (creates folder with settings.py)
-cd in music_controller and start django app api
    ---Note: in api/; -> models.py has the database models; views.py renders views or api endpoints; an endpoint is a location on the webserver you want to go to like /home)
-add apps to project settings -> api.apps.AppConfig (referencing AppConfig in apps.py) & rest_framework
-update databse
    ---Note: when starting the project or making a change to django internal database you need to update it with  makemigrations to detect the changes and migrate to apply them.

BackEnd: Creating An API Endpoint With Django Rest Framework - Build the database model
-write database model
-update database
-create serializer so the frontend can request data and receive it in json format
    --Note: serializer translates what's in models into a json response
-create an api view to let us view a list of all the different rooms
--create an urls.py in the api folder and link the api view class to a url
-include api url to the project urls file -> path('api/', include('api.urls'))

FrontEnd: Adding a frontend app with React
-start django app frontend
-in settings.py, add the frontend app in INSTALLED_APPS --> 'frontend.apps.FrontendConfig'
-cd frontend
-create static/, cd in, and create css/, frontend/ and images/
    --Note: static/frontend/ will contain a bundle of all the javascripts using the webpack library
-create templates/, cd in, create frontend/, cd frontend/, create index.html 
-back to music_controller/frontend/, create src/, cd src/, create components/ --will contain React components
-then terminal: 
npm init -y --> creates a package.json that npm will use to store all modules we need
npm i webpack webpack-cli --save-dev
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
npm i react react-dom --save-dev
npm install @material-ui/core
npm install @babel/plugin-proposal-class-properties
npm install react-router-dom
npm install @material-ui/icons
    --Note: babel is used to tranpile the code so it is compatible with older browsers
    --Note: webpack bundles all javascripts into one file and serves it to the browser
    --Note: material-ui is similar to bootstrap

-create babel.config.json and set up the babel loader by adding presets and plugins (to use async and await)
-create webpack.config.js and specify where to find the JS files (./src/index.js) and where to output the bundle (./static/frontend), also add module rules, optimization to make JS bundle smaller to laod faster in the browser, and plugins
-in package.json, add 2 scripts:
--"dev" will run webpack in development and watch mode (automatic recompiling when browser refreshed)
--"build" will run webpack in production mode

The idea is that django backend will render a page (an html template) and then React will manage it/take control of and fill in

-write the html in .music_controller/frontend/templates/frontend/index.html
-add the line to load the static folder {% load static %}
--Note: React will render its components into the <div id="app">
-add the script line that will grab the static folder that was specified at the top and combine it to frontend/main.js 
--Note: we just say "inside static go to frontend.main.js
--Note: we essentially just grab and load the bundled javascript that holds all of our React code from static/frontend/ 

-for django to render the template, add a function to frontend/views.py that will render the html. 
-create a urls.py and add a url from views
-include the frontend url to the project urls file
-in frontend/src/components,  add a App.js file and write the React code
-render that React component inside the index.html <div id="app":
--> const appDiv = document.getElementById("app");
--> render(<App />, appDiv);
-import App into index.js
--Note: so React will execute index.js that will import App.js that will render its page into the div located inside index.html
-cd back to root music_controller and run the backend --> python ./manage.py runserver 
-in a separate terminal: run the script "dev" that we added in package.json --> npm run dev
--Note: webpack will at index.js, which imports App; webpack will bundle everythings that's inside and output it in static/frontend
-in static/frontend, a main.js appears which contains the bundled up javascript

Adding styling and router
add some css in static/css/index.css
create three new components (pages) in src/components: HomePage.js, RoomJoinPage.js, CreateRoomPage.js
import BrowserRouter, Switch, Route, Link, Redirect in HomePage
in HomePage, add the Router and the different routes and which components they refer to inside the swith statements 
Note: <Route exact path='/'> -> if you don't put 'exact', any path that start with a '/' (i.e. /join, /create) will lead to the homepage.
To recap the process: 
-> the browser checks the list of urls of them project and see that anything different from admin or api leads to frontend/urls
-> frontend/urls.py imports function 'index' from frontend/views.py,
-> 'index' renders index.html,
-> index.html loads static as well as main.js that holds all of our React code (bundled javascript),
-> React execute index.js, which imports the class 'App' from App.js, 
-> App renders HomePage in index.html into the div with the id='app',
-> HomePage contains a Router which can switch among the home, join or create page,
-> to access thoses pages, they must be added to frontend/urls.py

Write a view to create a new room - backend
add a CreateRoomView class in api/views.py with a post method (empty (pass))
import APIView, response and status in views.py
add a CreateRoonSerializer in api/serializer.py with the needed fields for the post request
import CreateRoomSerializer to api/views.py
in api/models.py, in class Room, change: code = ... default = '' to default = generate_unique_code
Note: to know who the host is, we use a 'session key' so you don't need to sign in everytime the page is reloaded.
complete the post method:
- if session dores not exist, create one
- if the user is sending a valid request, check if the user already has a room ongoing
- if yes, update that room with new pause and skip data,
- if not (if the user does not have a room running), create one with host (session key created), pause and skip data
- otherwise, request bad request error
add create-room url

Add style and forms to the CreateRoomPage
import stuff from material-ui
add main grid
add sub-grid with title (typography)
add form (FormControl) with a text (FormHelperText), and add options (RadioGroup) with labels (FormControlLabel) with different colors
add a form with text field to vote for skipping a song
add two other forms for the buttons
Note: set a variable at the beginning of the class for the default value and set the onChange parameter to 
Note: set the onChnage parameters to the methods that will change the state of the data to be send to the backend

Add page to display the room info with the room code
create Room.js: create default state, add variable to get the roomCode from React's props.match.params, and render info
add route to HomePage with /room/:roomCode
add url t frontend.urls with 'room/<str:roomCode>'