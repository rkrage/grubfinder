GrubFinder - Food Truck API

Full stack (partially complete)

I did not have any experience with these technologies prior to writing this application (with the exception of PostgreSQL). These tools were chosen after doing research given the problem domain:

Flask (Flask.RESTful, Flask.SQLAlchemy) - a very lightweight and powerful Python framework that simplifies managing JSON REST endpoints and database interactions

Gunicorn - Python web server that is light on system resources (great for free Heroku account)

PostgreSQL - works well with Heroku and can handle large scale enterprise applications

Backbone.js - provides structure to javascript through MVC and allows simple asynchronous communication with JSON API

Google Maps API - used along with Backbone.js to give a visual representation of the data returned from the backend API


Currently, the frontend has very limited functionality (only displays food trucks near static location). I did not give myself enough time to code a fully functional frontend, but the javascript shows how easily the API can be harnessed in the future.

The backend API is complete but very minimal. Two REST endpoints are defined:

GET /api/foodtrucks/<int:id>
- id: food truck id in database
- returns a single food truck

GET /api/foodtrucks
- address (optional): street address
- latitude (optional: geographic coordinate
- longitude (optional): geographic coorinate
- if no parameters specified, returns list of all food trucks
- if latitude and longitude are specified, return a list of 20 food trucks within 3 km of coordinates (ordered by distance)
- if address is specified, lookup latitude/longitude and return a list of 20 food trucks within 3 km of coordinates (ordered by distance)

Future TODOs:

Finish frontend - Add search bar to find trucks by name/location and display on map.

Paginate API data - Currently, the /api/foodtrucks endpoint returns the entire list of food trucks. This should be paginated to save network resources.

Dynamic food truck database - Currently, the database contains static food truck information. Obviously food trucks will constantly be moving and the database should reflect that. In a perfect scenario, food trucks would register with the app and their location would be updated by posting to the API. If this cannot be accomplished, a daemon process would monitor the sfgov.org database and modify the local database with changes.

Web Testing - Use Selenium to test frontend web interface
