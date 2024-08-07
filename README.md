Youtube Clone

Welcome to the **Youtube Clone**! This project is a website developed using the Django framework. The site includes features for uploading and viewing videos, adding comments, likes, channel subscriptions, and more.

## Features

- **User Registration and Authentication**: Users can register, log in, and log out.
- **Video Upload**: Authorized users can upload videos with descriptions and previews.
- **Video Viewing**: All users can view uploaded videos.
- **Comments**: Authorized users can leave comments on videos.
- **Likes and Subscriptions**: Users can like videos and subscribe to other users' channels.
- **Editing and Deleting Videos and Comments**: Users can edit and delete their videos and comments.
- **Video Search**: Users can search for videos by title.

## Installation

Install Dependencies
Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
Install the required dependencies:

pip install -r requirements.txt
Project Configuration
Create a .env file in the project root and add the necessary settings:
env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
Apply Migrations and Start the Server
Apply the database migrations:

python manage.py migrate
Start the development server:

python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/ to view the site.

Usage
Registration and Authentication
Users can register and log in to access the site's extended features.

Video Upload and Viewing
After authentication, users can upload their own videos and view others' videos.

Commenting, Liking, and Subscribing
Users can leave comments, like videos, and subscribe to other users' channels.

Contributing
If you would like to contribute to the project, please fork the repository, make your changes, and create a pull request. All suggestions and improvements are welcome!

License
This project is licensed under the terms of the MIT License. See the LICENSE file for details.
