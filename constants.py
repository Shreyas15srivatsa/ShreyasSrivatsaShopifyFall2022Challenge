from enum import Enum

class Items(Enum):
  NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
  ERROR_INSERTING = "An error occurred while inserting the item."
  ITEM_NOT_FOUND = "Item not found."
  ITEM_DELETED = "Item deleted."

class WareHouses(Enum):
  NAME_ALREADY_EXISTS = "A warehouse with name '{}' already exists."
  ERROR_INSERTING = "An error occurred while inserting the warehouse."
  WAREHOUSE_NOT_FOUND = "Warehouse not found. Please try again."
  WAREHOUSE_DELETED = "Warehouse deleted."

WELCOME_MSG = 'Hello, Welcome to the Shopify Fall 2022 Developer Challenge attempt by Shreyas Srivatsa! Please follow the instructions in the README.md'