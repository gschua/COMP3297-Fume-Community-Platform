# COMP3297-Fume-Community-Platform

Final Project for the course COMP3297: Introduction to Software Engineering

### Required packages (run `pip install *`)

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

### How to Use

1. Install all required packages listed above.
2. In the terminal, go to project directory `cd .../<FCP_dir>`.
3. Run `python manage.py runserver`.
4. Go to Google Chrome and enter `127.0.0.1:8000` in the address bar.
5. To access FCP administration, enter `127.0.0.1:8000/admin` in the address bar.

### Standards:

 - Make all prices 1 decimal point ONLY or else CSS will break and have to redo everything.
 - 4 Spaces instead of 1 Tab.

### To-do List:

 - Figure out how to move all forms out of /vapoursite/views.py without breaking everything because right now it's cluttered and that's bad practice.
 - Lots of uploaded pictures end up being named "None*" which is weird but images are retrieved just fine so not really a huge issue.
 - Make footer stick to the bottom in form.html and cart.html.
 - Stop timezone from displaying in Transaction names.
 - Error messages when trying to add invalid objects to cart.
 - Make "Add to Cart" button disappear when have purchased game in all platforms.
 - Screenshots.
 - System Requirements.
 - Entire Review System.
 - Entire Search function.
 - Make Carousel in main.html get data from featured list
 - Clean up custom CSS.
 - Find some way to make it so that reward_threshold and reward_expiry can be edited by super users.
 - Function to inspect and expire Rewards.
 - Have the FCP run properly on other web broswers.
 - Implement tags as case-insensitive.
