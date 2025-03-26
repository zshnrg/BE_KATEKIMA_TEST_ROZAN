# Warehouse Stock Keeping Backend Server

This document provides instructions for running the backend server for warehouse stock keeping, which uses Django Rest Framework.

## Running the Server

1. **Run Migrations**  
  Apply database migrations to set up the database schema:  
  ```bash
  python manage.py migrate
  ```

2. **Start the Server**  
  Run the development server:  
  ```bash
  python manage.py runserver
  ```

## API Endpoints

Below is an explanation of each endpoint in the application:

### Items
- **`GET /items/`**  
  Retrieves a list of all items in the warehouse.

- **`POST /items/`**  
  Creates a new item in the warehouse.  
  Request body:
   - `name`
   - `unit`
   - `description`
   - `stock`
   - `balance`

- **`GET /items/:code/`**  
  Retrieves details of a specific item identified by its `code`.

- **`PUT /items/:code/`**  
  Updates the details of a specific item identified by its `code`.  
  Request body:
   - `name` (optional)
   - `unit` (optional)
   - `description` (optional)
   - `stock` (optional)
   - `balance` (optional)

- **`DELETE /items/:code/`**  
  Performs a soft delete on a specific item identified by its `code`.

### Purchases

#### Purchase Header

- **`GET /purchases/`**  
  Retrieves a list of all purchase records.

- **`POST /purchases/`**  
  Creates a new purchase record.  
  Request body:
   - `date`
   - `description`

- **`GET /purchases/:code/`**  
  Retrieves details of a specific purchase identified by its `code`.

- **`PUT /purchases/:code/`**  
  Updates the details of a specific purchase identified by its `code`.  
  Request body:
   - `date` (optional)
   - `description` (optional)

- **`DELETE /purchases/:code/`**  
  Performs a soft delete on a specific purchase identified by its `code`.

#### Purchase Details

- **`GET /purchases/<str:header_code>/details/`**  
  Retrieves detailed information about a specific purchase, identified by its `header_code`.

- **`POST /purchases/<str:header_code>/details/`**  
  Creates a new purchase detail record.  
  Request body:
   - `item_code`
   - `quantity`
   - `unit_price`
   - `header_code`

### Sells

#### Sell Header

- **`GET /sells/`**  
  Retrieves a list of all sell records.

- **`POST /sells/`**  
  Creates a new sell record.  
  Request body:
   - `date`
   - `description`

- **`GET /sells/:code/`**  
  Retrieves details of a specific sell identified by its `code`.

- **`PUT /sells/:code/`**  
  Updates the details of a specific sell identified by its `code`.  
  Request body:
    - `date` (optional)
    - `description` (optional)

- **`DELETE /sells/:code/`**  
  Performs a soft delete on a specific sell identified by its `code`.

#### Sell Details

- **`GET /sells/:header_code/details/`**  
  Retrieves detailed information about a specific sell, identified by its `header_code`.

- **`POST /sells/:header_code/details/`**  
  Creates a new sell detail record.  
  Request body:
    - `item_code`
    - `quantity`
    - `header_code`

### Report
- **`GET /report/:item_code/`**  
  Retrieves a report for a specific item identified by its `item_code`.  

  **Query Parameters**:  
  - `start_date` (optional): Filter the report to include data starting from this date. Format: `YYYY-MM-DD`.  
  - `end_date` (optional): Filter the report to include data up to this date. Format: `YYYY-MM-DD`.  
  - `pdf` (optional): If set to `true`, the report will be generated as a PDF file. Default is `false`.  

Use these endpoints to interact with the backend server for managing warehouse stock.  