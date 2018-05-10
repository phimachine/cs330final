Final project

Final project uses Yelp API and collects user data, because collecting user data is what's popular these days.

## A database 3-4 tables
### A user table.
Passwords, emails, account information.

### A table with queried restaurants, uniquely identified.

### A visit table.
Maps users to restaurants that they have been to. One to many from user to restaurants.

### A inferred table.
Updates the purchase power of each user. One to one mapping.

## Major interfaces
### Log in page for the user.
WTForm.

### User information editing panel.
WTForm.

### Search engine interface that queries for the restaurants.
WTForm.

### Restaurant presentation.
It's better to have the map information presented as a panel on the left or right.

There should be a "I've been there" button to click on.

There should be an OpenWeather panel that displays weather.

There should be a "next" button that allows the user to move on to the next restaurant.

## Controllers
Login controller.

Search controller.

User information editing panel.

## AJAX API.
"next" button on the restaurant presentation should be AJAX.
