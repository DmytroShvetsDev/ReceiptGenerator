# Receipt Generator


This is a service for generating receipts for a restaurant chain.  The api accepts a receipt as a JSON file and saves it to the database. And also, using Celery and Redis, it launches asynchronous tasks to generate PDF files for these receipts for their further printing.
The API has the following database structure:



## Run with Docker

Docker must be already installed!

```shell
git clone https://github.com/DmytroShvetsDev/ReceiptGenerator.git
cd ReceiptGenerator
touch .env
docker-compose up --build
```
For Windows, the command "touch .env" will be "echo > .env"

For an example of filling out .env, see .env.sample!


### For Sign in, you can use: 
 - username: admin
 - password: adminuser


### The API supports the following endpoints:
- using /admin/ --- Work with admin panel
- using /api/schema/swagger/ --- API documentation by swagger
- using [GET] /api/printers/ --- Return list all printers
- using [POST] /api/printers/ --- Create printer
- using [GET] /api/printers/{id}/ --- Return the detail page for the printer, where you can view all receipts for this printer
- using [PUT, PATCH] /api/printers/{id}/ --- Empty request change recipts.status for all receipts for this printer rendered -> printed
- using [POST] /api/receipts/create/ --- this endpoint accepts JSON from ERP. (Ex. {"point_id": 1,"order_number":
        1,"type": "client","order_data": [{"name": "banana","price": 20,"count": 2},...]}). 
        
    creates checks in the database and runs a worker to generate PDFs for these checks.
- using [GET] /api/receipts/list/ --- This endpoint displays all checks

#### you can also see the detailed documentation in the api.yml file