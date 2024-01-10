### An invoice management website, with the following api calls :
#### -- /api/invoices/
#### -- /api/invoices/\<int:pk\>

### Here, we can perform crud operations for the following models:
#### -- Invoice model fields -> date (automatically current date), invoice_number (primary key, integer, auto increment), customer_name
#### -- InvoiceDetail model fields -> invoice (ForeignKey), description, quantity, unit_price, price

### We can create an invoice with a customer name and also create/update the associated invoice details (description, quantity, unit_price) as the payload in /invoices/ api
