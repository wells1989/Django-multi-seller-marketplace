## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Project Notes](#project-notes)

## Description

This Full Stack Django application is a multi-seller marketplace, where users can log in and sell their products, in addition to viewing their own purchases / sales statistics and leaving ratings for the products they have purchased.

**Tech-stack: python / JavaScript / SQL / tailwindCSS / html**

**Project Areas: Django authentication models / Advanced MVT architecture / inter-model relationships between Django models / Django database modelling and utilising data in UI integration / JavaScript for DOM manipulation / cart and checkout implementation with stripe API / dynamic UI displays using chartJS**

## Installation

1. Clone the repository:

   ```bash
   gh repo clone wells1989/Djando-multi-seller-marketplace

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

3. Apply database migrations:

   ```bash
   python manage.py migrate 

4. Run the development Server:

   ```bash 
   cd mysite
   python manage.py runserver 

Access the app at http://localhost:8000 in your web browser.

## Usage

### User Registration / Login
- **Description:** Allows users to register or log in to the platform.

![Screenshot (527)](https://github.com/wells1989/Full-stack-blog/assets/122035759/53f46a8b-60e8-4a76-ab12-928841cd3f13)
![Screenshot (528)](https://github.com/wells1989/Full-stack-blog/assets/122035759/4dfe9730-c372-4578-a664-cb0462852f4f)

### Homepage
- **Description:** Displays a dynamic homepage with featured products and links via the Navbar to the other areas if the User is logged in / authenticated

![Screenshot (549)](https://github.com/wells1989/Full-stack-blog/assets/122035759/f61bf836-9dad-46db-a829-38f922eb4510)

### Creating new product
- **Description:** Provides a form for users to create and list new products for sale.

![Screenshot (535)](https://github.com/wells1989/Full-stack-blog/assets/122035759/554fb789-80d7-4560-89fe-9ac7d599342b)

### Product details / purchasing
- **Description:** Product Details page which allows you to add or remove items from your cart

![Screenshot (550)](https://github.com/wells1989/Full-stack-blog/assets/122035759/c85bdac7-d454-4b1e-8686-031e2fd0fa7b)

- **Description:** cart View provides overview of Cart (Items / quantity / total price) before checking out

![Screenshot (537)](https://github.com/wells1989/Full-stack-blog/assets/122035759/e9bd9430-8a78-4cef-b661-4be4f97892b3)

- **Description:** On Checkout, accessing the stripe API for payment

![Screenshot (539)](https://github.com/wells1989/Full-stack-blog/assets/122035759/7777ac90-f6c9-4c5a-bd3b-00353971c699)

### Viewing sales dashboard
- **Description:** Users can view / edit / delete their items, as well as seeing the sales / revenue and average rating for each
- **NOTE: superusers can access everyone's items**

![Screenshot (530)](https://github.com/wells1989/Full-stack-blog/assets/122035759/57dc1ebe-e7f3-435c-af28-1ea67c6191de)

### Viewing sales statistics
- **Description:** Users can retrieve sales data for their products, seeing the total sales or sales by time period, in table or chart form
- **NOTE: superusers can see entire sales across users**

![Screenshot (547)](https://github.com/wells1989/Full-stack-blog/assets/122035759/67ecd1ee-38ca-49b6-a89f-094a5e4a2e6f)
![Screenshot (548)](https://github.com/wells1989/Full-stack-blog/assets/122035759/cf2bdd3b-c93d-47be-ada0-4e7b30f2a56a)

### Viewing your purchases
- **Description:** Users can view the orders they have made, as well as the amount they paid and can also leave a 1-5 star rating for the products

![Screenshot (544)](https://github.com/wells1989/Full-stack-blog/assets/122035759/113395b5-64c9-47ba-94b9-a48b191c5a39)


### Project Notes:
- The Focus of this project was to provide a wide view of functionality, including user authentication, model instance manipulation via Django forms / views with ORM and UI statistics obtained from SQL databases.
- The App is designed to be used by both regular users and superusers, with superusers having more permissions on editing / deleting products, as well as being able to view the entire sales across the site.
- The Stripe Authentication was used with a dummy payment_intent due to an internal Stripe error when developing the product

#### Future-development:
- A future feature could be adding a comments section to the product reviews. This would require a separate Review Model, which could then be linked to a product whilst having it's own comments and review field.
- A User profile section onthe main site would allow users to customise and alter their Profile information in the event of changing email addresses etc.
- The login feature could have incorporated a change password reset in case the user forgot their password.
