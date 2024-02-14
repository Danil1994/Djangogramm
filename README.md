# Djangogramm

An application similar to Instagram, which we named Djangogramm. This application has a web interface and offers the
following functionalities:

Registration and Confirmation;
Post Creation and Viewing;
Feed of Latest Posts;
Restricted Access for Guests;

link to UML-diagrams
`models - https://drive.google.com/file/d/1i-Auyu0iFgj87nUHLyb_s4vJ-KUphytt/view?usp=sharing`
`pages - https://drive.google.com/file/d/1_Z9TZ3NYJAc8bkPw2vy6mIVHadlal85g/view?usp=drive_link`

## install

1. Clone repo:
  --Clone with SSH `git clone https://github.com/Danil1994/Djangogramm.git`
  --Clone with HTTPS `git clone git@github.com:Danil1994/Djangogramm.git`

2. Go to your project folder: `path/to/the/Djangogramm`
3. Load your .env file like .env.example. And provide all the required information (passwords, secret keys etc).
4. Install requirements.txt: `pip install -r requirements.txt`
5. Create a database and configure connection parameters
6. Connect your cloud storage for your app`s photo.
7. Make migrate:  `python manage.py migrate`

## Run

1. Run server: `python manage.py runserver`
2. Go to link `http://localhost:8000` in your browser.

## Using

Registration and Confirmation:
Users can register on our website using their email addresses. After completing the basic registration, each user
receives a unique confirmation link. By simply clicking on this link, the user is automatically redirected to their
profile page, where they can add their full name, bio, and avatar.

Post Creation and Viewing:
Users can create posts with images and add multiple images to each post. Additionally, each post can be tagged with
multiple tags. Users have the ability to like posts and also remove their
likes and write comment.

Feed of Latest Posts:
Our users can view posts from other users through a convenient feed of the latest publications. This feature allows
users to stay up to date with all the new posts.

Restricted Access for Guests:
Unauthorized guests do not have access to user profiles and photos. To view content, a user must be registered and
logged in.

## Create fake data.
Using python -m main_app.create_fake_data to create fake data in th app (posts, users, comment, ect.) 
!WARNING! 
Using `python -m main_app.create_fake_data` you create new photo in the folder "task_11/media/photos". But if you 
drop your DB you don`t delete this photo. So if you wont to do it you must clean this folder separately.

## Admin panel.
They are created superuser. With next parameters:
--username: admin
--email: one12@mail.com
--password: 1111
Enter it to access the admin panel.

## Help to develop

1. Fork the project
2. Create new branch: `git checkout -b feature/new_ability`
3. Commit new changes: `git commit -m 'Add new'`
4. Push changes: `git push origin feature/Add new`
5. Create request to update repo (Pull Request) на GitHub
