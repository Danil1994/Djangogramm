# Djangogramm

An application similar to Instagram, which we named Djangogramm. This application has a web interface and offers the
following functionalities:

* Registration and Confirmation;
* Post Creation and Viewing;
* Feed of Latest Posts;
* Restricted Access for Guests;
* Possibility to like/dislike and write comments, subscribe;

## Install

1. Clone repo:
   --Clone with SSH `git clone https://github.com/Danil1994/Djangogramm.git`
   --Clone with HTTPS `git clone git@github.com:Danil1994/Djangogramm.git`

2. Go to your project folder: `path/to/the/Djangogramm`.
3. Load your .env file like .env.example. And provide all the required information (passwords, secret keys etc).
4. Activate your virtual env.
5. Install requirements.txt: `pip install -r requirements.txt`.
6. Create a database and configure connection parameters.
7. Connect your cloud storage for your app`s photo. !!!WARNING!!! You have to create 'avatars' and 'photo' folders in
   your folder.
8. Make migrate:  `python manage.py migrate`.

## Run

1. Run server: `python manage.py runserver`
2. Go to link `http://localhost:8000` in your browser.

## Using

* Registration and Confirmation.

Users can register on our website using their email addresses or login via third-party services (google, github).

* Post Creation and Viewing.

Users can create posts with images and add multiple images to each post. Additionally, each post can be tagged with
multiple tags. Users have the ability to like/dislike posts and write comment.

* Subscribe.

Users are able to visiting others users profile and subscribe. After users will see the latest posts from them
subscribes

* Restricted Access for Guests:

Unauthorized guests do not have access to user profiles and photos. To view content, a user must be registered and
logged in.

## Create fake data.

Using `python -m main_app.create_fake_data` to create fake data in th app (posts, users, comment, ect.)
Fake photo are in the 'media/fake_photos/'
