# Changelog

### 2017-04-25
 - Got a new logo!
 - General syntax clean up.
 - Update to Member model field to distinguish between regular and super users. Provided super users wuth elevated permissions.
 - Deprecated Admin model field.
 - Fully implemented system for choosing of featured games for super users (aka administrators). Creation of new template for this feature.
 - Update layout of Signup and Login pages.
 - Fully implemented system to change email address.
 - Deprecated MemberTag model field. Tag is now the sole tag model. Updated all related functions, views, models, and templates to adapt to new feature.
 - Separated the header and footer on all templates into their own template files for modularization. Will no longer need to change the header in every single template whenever changes are made.
 - Seperated cart implentation into its own folder.
 - Wrote function to find most popular tags for a game.
 - Implemeted browse purchased games.


### 2017-04-13
 - Implement system for lost password requests by sending of token via email. Members can then enter a new password. Fully integrated with database.
 - Wrote function to create custom lists of recommended games for each member based on tag-similarity.
 - Main and Game pages can now retrieve most dynamic data (recommended games, featured games, game details, etc.).
 - Most hyperlinks are currently working. Game and Cart pages have dynamic URLs.
 - Can now choose preferred platform when adding game to cart. Apply restrictions (e.g. have already bought game) (missing error messages).
 - Rewards and purchasing system are fully functional (only missing error messages).
 - Fully implement adding and deleting of tags (restricted to members who have purchased the game).
 - General bug fixes.


### 2017-04-10
 - Implemented fully-realized account and authentication system for the FCP.
     - Registration
     - Validation of username, password, and email address.
     - Logging In
     - Logging Out
     - Checking login status throughout all views
     - Updated headers of all templates to dynamically detect login status
 - Update to Member model to integrate with authentication system
 - Implemented authentication using GitHub


### 2017-04-05
 - Researched best practices and OOP principles. Overhauled file tree of entire project.
 - Implemented renaming of images upon upload based on corresponding owner's ID.
 - Significant changes to models.py, finalized general database model (minor changes may be implented later on).
 - Overhauled model framework, implemented framework changes.


### 2017-03-29
 - Plan out model framework and architecture.
 - Implemented prototype model framework.
 - Implemented entire admin view. Can now view and edit database with ease.
 - Implement rewards pop-up on main page.
 - Implement game detail page.
     - Upon going to a game's page, view it's details such as platform, release date, etc.
     - Dynamically pull different data based on URL.
     - Can add games to cart via this page.
     - Can add tags to game (does not check yet if member has purchased game).
     - Fully integrated with database.
 - Implement cart page.
     - Can see games that have been added to the cart, their price, and other details.
     - Can see how many rewards member currently has.
     - Can apply or remove rewards to and from cart. Member's Reward's will correspodingly be added or deleted.
     - Can remove games from cart and empty the cart.
     - Fully integrated with database.

### 2017-03-15
 - Project started, initial commits
 - Create user interface executable prototypes.
