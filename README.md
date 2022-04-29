## Shopify Fall 2022 Developer Intern Challenge

### Task:
Build an inventory tracking application for a logistics company. This is an open-ended task, with a heavy focus on the quality of the backend code. 

## Features:
* Add a warehouse/location
* Edit a warehouse/location
* Delete a warehouse/location
* Add items to the inventory of a specific warehouse/location
* Edit price, description, and warehouse/location of a particular item
* Delete the item from the inventory

In essence, we can perform CRUD operations on the items in the inventory, as well as the ability to create warehouses/locations and assign inventory & items to the warehouse (Extra feature #2 from the list)


Since we are only interested in evaluating the quality and functionality of the backend code, the application was designed as an APIl with no front-end interface. To test the application, one would need to execute cURL commands against the endpoints, or use the Postman collection provided in the `tests/` folder. 

## Tech Stack:
* Python
  * Flask App
  * Marshmallow for schema validation
* Flask-SQLAlchemy for backend
* Postman for testing

## Links:
* Replit hosted link - https://replit.com/@ShreyasSrivatsa/ShreyasSrivatsaShopifyFall2022Challenge#README.md
* Github hosted code link - https://github.com/Shreyas15srivatsa/ShreyasSrivatsaShopifyFall2022Challenge

## How to run the API?
Please click on the Replit hosted link provided above. Once you navigate to the Replit hosted application, please click on the green "run" button on the top right corner. 

Once you run it, you'll see a simple landing page containing basic instructions. The application will run on port `3000` and the base URL to interact with the API is 

``` https://shreyassrivatsashopifyfall2022challenge.shreyassrivatsa.repl.co/ ```

Once the application is running, we can hit some of the endpoints either through cURL, or Postman. 


### Add warehouse:
For example, to add a new warehouse, one would need to execute the cURL command 

``` 
curl --location --request POST 'https://shreyassrivatsashopifyfall2022challenge.shreyassrivatsa.repl.co/warehouse/warehouse_1'
```

### Add item:

To add an item to the inventory, one would need to run the cURL command 

```
curl --location --request POST 'https://shreyassrivatsashopifyfall2022challenge.shreyassrivatsa.repl.co/item/desk' \
--header 'Content-Type: application/json' \
--data-raw '{
  "price": 75.99,
  "description": "This is a foldable desk",
  "warehouse_id": 1
}' 
```

### Edit Item:

```
curl --location --request PUT 'https://shreyassrivatsashopifyfall2022challenge.shreyassrivatsa.repl.co/item/desk' \
--header 'Content-Type: application/json' \
--data-raw '{
  "price": 55.99,
  "description": "This is a foldable desk",
  "warehouse_id": 1
}'
```
### Delete Item:

```
curl --location --request DELETE 'https://shreyassrivatsashopifyfall2022challenge.shreyassrivatsa.repl.co/item/desk' \
--header 'Content-Type: application/json'
```

### Delete Warehouse:

```
curl --location --request DELETE 'https://shreyassrivatsashopifyfall2022challenge.shreyassrivatsa.repl.co/warehouse/warehouse_1'
```

and so on... 

## Testing:
In the tests folder, a Postman collection has been provided. The testing suite can be gathered in Postman by importing the json collection into Postman. 

Once the testing suite has been setup, there's around 40 tests on Postman that can be run. They can be run individually or as a collection in the collection runner. I have included some verification and testing in Postman, and as a result, this would be a great way for us to test the web API. 

## Additional features:
Apart from the basic features such as CRUD on items, ability to create and delete warehouses, I have also added validation to several endpoints

* If one tries to delete a warehouse that contains some items in it's inventory, we throw an error and prevent such an operation
* If one tries to add an item to an inventory of a warehouse that doesn't exist/registered with the application, we valiidate the `warehouse_id` and throw an error if the validation fails
* The same is applicable if one tries to edit the `warehouse_id` of an item to an unknown `warehouse_id`
* I have used Marshmallow for schema validation, serialization and deserialization from SQLAlchemy objects to JSON objects and vice-versa.
* Followed a modular, clean, and object-oriented programming approach to produce quality, industry-standard code
