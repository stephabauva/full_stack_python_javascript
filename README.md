# full_stack_python_javascript

Set up:
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

FrontEnd: Adding a frontend app with React:
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

Adding styling and router:
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

Write a view to create a new room - backend:
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

Add style and forms to the CreateRoomPage:
import stuff from material-ui
add main grid
add sub-grid with title (typography)
add form (FormControl) with a text (FormHelperText), and add options (RadioGroup) with labels (FormControlLabel) with different colors
add a form with text field to vote for skipping a song
add two other forms for the buttons
Note: set a variable at the beginning of the class for the default value and set the onChange parameter to 
Note: set the onChnage parameters to the methods that will change the state of the data to be send to the backend

Add page to display the room info with the room code (v7):
create Room.js: create default states (values at false at first, link to the backend later), add variable to get the roomCode from React's props.match.params, and render info
add route to HomePage with /room/:roomCode
add url to frontend.urls with 'room/<str:roomCode>'
create the get request getRoom to get the data
add the url to api.urls
try http://127.0.0.1:8000/api/get-room?code=SZSLTA in browser; ...?code=hello should not work
add function getRoomDetails to Room to fetch the data from the backend
call that function with this.getRoomDetails() in Room Constructor that will update the state and force a re-render 
Note: add toString() to {this.state.guestCanPause} and {this.state.isHost} to eb able to see the result in the browser
in CreateRoomPage.js, modify handleRoomButtonPressed() with React props.history.push() so that when when press create a room, we get directed to the right page --> this.props.history.push('/room/' + data.code)

add content to join the room page and hook it to the backend (vid 8):
in RoomJoinPage, add default states, and layout for the textfield and the buttons
in api/views, add the JoinRoom class that will check the data attached to the room code in the DB
if some data exists - if len(room_result) > 0 - add the room code to the session data: self.request.session['room_code'] = code
Note: now if the user leaves, it won't need to re-enter the room code of the last session when he comes back
Note: the session data and room data (in DB) are two separate things
add the path('join-room', JoinRoom.as_view()) to api/urls
in RoomJoinRoom, add the fetch request in the roomButtonPressed method and add it to the onClick key

Styling the homepage and redirecting the user to his room (v9)
The idea: When we go to the homepage , we need to call the endpoint to check if the user is already in a room. 
Note: we add a async to the componentDidMount method so that the rest of the application does not wait for the method to finish/backend response (to check if the user is already in a room and so get redirected to it)
Note: React's LifeCycle Methods like componentDidMount are things you can hook into to alter the behavior of a component. componentDidMount() is a hook that gets invoked right after a React component has been mounted aka after the first render() lifecycle.
Note: componentDidMount is a lifecycle hook. It doesn't need to be called/invoked directly
Add styling to HomePage (add ButtonGroup tp have the buttons side by side; disableElevation removes the shadows)
Add view to api/views to get the room code based on the user session
Add the url to aip/urls
in homePage, set a state for roomCode and fetch the actual roomCode data to componentDidMount
in HomePage Router, add what to render --> which page to redirect depending on if the user is already in a room or not
Note: if he is in a room then redirect to that room, if not redirect to the homepage

Adding functionality to leave the room and go back to HomePage (v10)
in views, create a post request in a class LeaveRoom
pop the room_code from the user session data
get the user code (session_key)
delete all room data attached to the session key
add the url
when the page render we need to reset the state of the room code to null, otherwise even we delete it from the database it will still be present as a state --> add a clearRoomCode method and setState of roomCode to null
in the Route of the Room page, render Room with its props (roomCode: "WGGVFK" in match.params is the one we need) and also add a call back to the props: leaveRoomCallback
Note: props are provided in HomePage by Route
Note: a call back allows a child component to alter a parent component
in Room. leaveRoomCode is used in getRoomDetails and leaveButtonPressed to clear any roomCode previously set as state

Adding settings feature for the host to modify the room page (v11)
add updateRoom class in views with a patch method (need the room code, guest_can_pause and votes_to_skip data)
add a serializer (updateRoomSerializer) to pass the data from the request to the view
Note: in models.py the code field needs to be unique, which will pause a pb when we want to update the room since we need to pass a room code that already exists; it's not unique.
Note: so we redefine the code field (from models.py) right in the serializer. Now, code will be referencing this field --> serializers.CharField(validators=[]) and not the one in models where code needs to be unique.
Note: also add a security to check if the person doign the update is the host of the page in case of hack
add the url
in Room.js add a settings button with a showSettings default value to false in the constructor 
add an updateShowSettings method that can setState of showSettings
bind updateShowSettings's this to the the this of the class
add the renderSettingsButton method that will change the value of showSettings to true 
add the line that will render the button if the user is the host of the room --> {this.state.isHost ? this.renderSettingButton() : null}
add the renderSettings method that will return the settings page instead of the room page
Note: the settings is the createRoomPage with some tweeks
in renderSettings, add a back button to the room page
in Room' render, add an if statement that will render the settings page if the settings button is presssed; and thus showSettings state is true, otherwise render the room page
bind this of renderSettingsButton and renderSettings to this of class
