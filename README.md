# CCD Clothing Shop Web Application

## Overview
The Clothing Shop web is finished. Below is an overview of its functionalities and database usage:

## Getting Started
Test the application in Render.com now:
[Clothing Shop Web Application](https://ccd-clothingshop.onrender.com/)

## Final return features

- **User Registration and Login:** Securely register and log in to access the platform's features.
- **Clothes Listings:** Add your clothes for sale and browse listings from other users. Each listing includes details such as brand, size, price, and description.
- **Modify and Delete Listings:** Own a listing? You can modify its details or delete it entirely.
- **Virtual Currency Transactions:** Buy clothes from other users using virtual currency. Add to your balance to continue shopping.
- **Messaging:** Communicate with other users about items through the built-in messaging system. Keep track of your conversations in the user tab.
- **User Dashboard:** View available, sold, and bought listings. Manage your chats and replies within the user tab.
- **Admin Privileges:** Admins can modify or delete any listing, add listings to "Admin Picks" for featured visibility, and manage the site's overall content.

### Database Structure

The application utilizes a robust PostgreSQL database consisting of 11 tables to store and manage data efficiently:

1. **Categories:** Different clothing categories.
2. **Chats:** User communications about transactions.
3. **Clothes:** Details of clothes listed for sale.
4. **Images:** Byte data of images for each listing.
5. **Messages:** Messages exchanged between users.
6. **Sizes:** Clothing sizes.
7. **Transactions:** Completed purchase information.
8. **Users:** User account details, including balance.
9. **Subcategories:** More specific categories like t-shirts or jeans.
10. **Category_Sizes:** Item sizes for different categories.
11. **Brands:** Clothing brands.

### 3rd return Features
- **Production:** Clothing shop is running on render.com
- **Virtual Currency System:** Users can deposit virtual money to buy clothing items.
- **Messaging System:** Users can communicate with buyers and sellers through messages.
- **Search Functionality:** Users can search for specific clothing items.
- **Listing Management:** Users can list their own clothing items for sale.
- **Chat History:** Users have access to their chat history.
- **Item Modification and Deletion:** Users can modify and delete their listed items.
- **Admin Privileges:** Admins can edit or delete items as well.
- **Database Tables:** The application's database is structured with nine PostgreSQL tables:
    1. **Categories:** Stores information about different clothing categories available on the platform.
    2. **Chats:** Facilitates communication between users regarding purchases, inquiries, or negotiations.
    3. **Clothes:** Contains details about individual clothing items listed for sale, including brand, size, price, and description.
    4. **Images:** Stores byte data images associated with each clothing item.
    5. **Messages:** Records messages exchanged between users during transactions.
    6. **Sizes:** Stores clothing sizes.
    7. **Transactions:** Tracks information about completed transactions, including purchase amount.
    8. **Users:** Contains user account information, including usernames, encrypted passwords and balane.


### 2nd return Features
- **Homepage Categories and Brands:** The homepage displays categories and brands that users can click on to browse clothes in those categories.
- **User Authentication:** Users can create an account, log in, and log out of their accounts.
- **Clothes Selling:** Logged-in users can add clothes for sale using a form, including the option to upload pictures which are saved in a designated folder.
- **Database Structure:** The application utilizes nine PostgreSQL database tables: Categories, Chats, Clothes, Images, Messages, Sizes, Transactions, Users, and Admin Picks.
- **Footer Navigation:** The footer contains links to pages such as "About Us" and "FAQ" for additional information and frequently asked questions. Users can also navigate back to the home page.

Thank you!
