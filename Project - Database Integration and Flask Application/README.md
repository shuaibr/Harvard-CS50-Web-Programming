# Project 1

One of the most enjoyable project's I've worked on.

This is a full-stack project where my goal was to build a book review website.

Using Flask and Python as my backend, I was able to build a system that allowed Users to register for the website and then log in using their username and password. Flask was a key tool here, I used WTForms to validate user registration and used sessions to presist user data across all pages. Since this project was completed for the Harvard Web Dev project, I'd like to include sanitization to prevent SQL injection and include SHA256 encryption from my Cryptography project.

Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. I integrated a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. This part of the project was so much fun. I am an avid reader and I was planning on integrating a book recommender system into my website and this project allowed me to get started on implementing a database as the foundation of this system.

Finally, users will be able to query for book details and book reviews programmatically via my website’s API. Essentially, I created a very simple GET call API to allow users to access book review information using an ISBN identity. The ISBN is an internationally recoginzed unique identifier for all books.
