# Clothing Shop Web Application

## Getting Started
To start the application:
1. Install requirements: `pip install -r requirements.txt`
2. Create a file named `.env` in the root directory of the project.
3. Add the following lines to the `.env` file, replacing placeholders with your actual database URL and secret key:
    ```plaintext
    DATABASE_URL="postgresql://user:password@localhost:5432/databasename"
    SECRET_KEY="setasecretkeyhere"
    ```
4. Sign in to your PostgreSQL database.
5. Create a new database using the provided database URL.
6. Run the schema.sql commands to set up the database schema.
7. Run the app: `flask run`

## Overview
The Clothing Shop web application is currently under development and making progress. Below is an overview of its current functionalities and future enhancements:

### Current Features
- **Homepage Categories and Brands:** The homepage displays categories and brands that users can click on to browse clothes in those categories.
- **User Authentication:** Users can create an account, log in, and log out of their accounts.
- **Clothes Selling:** Logged-in users can add clothes for sale using a form, including the option to upload pictures which are saved in a designated folder.
- **Database Structure:** The application utilizes five PostgreSQL database tables: Brands, Categories, Clothes, Sizes, and Users.
- **Footer Navigation:** The footer contains links to pages such as "About Us" and "FAQ" for additional information and frequently asked questions. Users can also navigate back to the home page.

### Future Enhancements
- **User Profile Tab:** Implement a user profile tab where users can view their own listings and manage their account information.
- **Contact Sellers:** Provide a way for users to contact sellers directly through the application.
- **Purchase Functionality:** Enable users to buy clothes listed by sellers through the application.
- **Detailed Item View:** Allow users to click on an item to view detailed information in another tab or modal.
- **Admin User:** Implement an admin user role with special privileges for managing users, listings, and other aspects of the application.
- **Security Measures:** Enhance security measures to protect user data and prevent unauthorized access.
- **Multiple Images per Listing:** Allow sellers to add more pictures of a garment to their listings for better showcasing.
- **User Interface Improvements:** Enhance the appearance and user experience of the application to make it more visually appealing and user-friendly.

Thank you!
