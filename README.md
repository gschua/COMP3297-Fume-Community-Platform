# COMP3297-Fume-Community-Platform

Final Project for the course COMP3297: Introduction to Software Engineering

# Required packages (run `pip install *`)

 - Django (dependencies: pytz)
 - Pillow (dependencies: olefile)
 - django-crispy-forms
 - social-auth-app-django
	 - six (required by pip)
	 - social-auth-core
	 - oauthlib
	 - requests-oauthlib
	 - defusedxml
	 - python3-openid
	 - PyJWT
	 - requests
 - python-social-auth (same dependencies as social-auth-app-django)

# How to Use

1. Install all required packages listed above.
2. In the terminal, go to project directory `cd .../<FCP_dir>`,
3. Run `python manage.py makemigrations`, then answer yes to all prompts,
4. Run `python manage.py migrate`.
5. Run `python manage.py runserver`.
6. Go to Google Chrome and enter `127.0.0.1:8000` in the address bar

---

# In This Branch

## Important changes and new features:
 - Main can find featured and recommended games
 - Main can retrieve data of featured/recommended games from database (aka display dynamic data)
 - Most hyperlinks are currently working. Game and Cart pages now have dynamic URLs based on Game/Member ID
 - Game pages can retrieve dynamic data (except for reviews and other unneccessary hard coded stuff)
 - Can add game to cart through the Game page. Can choose platform to use.
 - Will not add game to cart if that specific game and platform combination has already been chosen before. Will not add game to cart if platform chosen is not one that the game is available on.
 - Rewards system and Purchasing system are fully functional (but otherwise missing some UI necessities).
 - Upon first registering with the FCP, get a free 5 rewards (requirement by TAs, but not written in project description).

## New and Edited files:
```
/accounts/views.py
/fume/forms.py
/fume/models.py
/static/style/main.css
/templates/vapoursite/cart.html
/templates/vapoursite/form.html
/templates/vapoursite/game.html
/templates/vapoursite/main.html
/vapoursite/settings.py
/vapoursite/urls.py
/vapoursite/views.py
```

## Other changes:
 - Deleted /templates/vapoursite/deprecated because they're identical to the UI Prototypes
 - Deleted /templates/vapoursite/reward.html and search.html because we won't be working on these functions yet for now. Will copy over template from User Interface Prototypes later on.
 - Moved User Interface Prototypes directory under /docs.
 - Renamed /templates/vapoursite/game-detail.html to game.html
 - Renamed /static/style/prototype.css to main.css
 - Renamed /static/style/game-detail.css to game.css

## Standards:
 - Make all prices 1 decimal point ONLY or else CSS will break and have to redo everything.
 - 4 Spaces instead of 1 Tab.

## To-do List (that's not in the Project Description probably):
 - TAGGING SYSTEM
 - Figure out how to move all forms out of /vapoursite/views.py without breaking everything because right now it's cluttered and that's bad practice
 - Lots of uploaded pictures end up being named "None*" which is weird but images are retrieved just fine so not really a huge issue.
 - Make a navbar.html so no need to keep copy-pasting the navbar everywhere
 - Add an icon in the header of all html files
 - Make footer stick to the bottom in form.html and cart.html
 - Add ending comments to all divs in all html files
 - Stop timezone from displaying in Transaction names
 - Actually write a function to retrieve most popular tags for a game
 - Error messages when trying to add invalid objects to cart
 - Make "Add to Cart" button disappear when have purchased game in all platforms
 - Screenshots
 - System Requirements
 - Entire Review System
 - Entire Search function
 - Make Carousel in main.html get data from featured list
 - Clean up custom CSS
 - Find some way to make it so that reward_threshold can be edited from admin
 - Find better way to calculate Reward.expiry_date
 - Function to inspect and expire Rewards
 - Have the FCP run properly on other web broswers
