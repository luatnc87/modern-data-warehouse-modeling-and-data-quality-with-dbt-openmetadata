// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table dim_address {
  address_key integer [primary key]
  addressid integer
  city_name varchar
  state_name varchar
  country_name varchar
}

Table dim_order_status {
  order_status_key integer [primary key]
  order_status varchar
}

Table dim_credit_card {
  creditcard_key integer [primary key]
  creditcardid integer
  cardtype varchar
}

Table dim_product {
  product_key integer [primary key]
  productid integer
  product_name varchar
}

Table dim_customer {
  customer_key integer [primary key]
  customerid integer
  fullname varchar
  businessentityid varchar
  storebusinessentityid varchar
  storename varchar
}

Table dim_date2 {
  date_key integer [primary key]
  date_day date
}

Table fct_sales {
  sales_key varchar [primary key]
  salesorderid varchar
  salesorderdetailid varchar
  product_key varchar
  customer_key varchar
  ship_address_key varchar
  creditcard_key varchar
  order_date_key varchar
  order_status_key varchar
  unitprice varchar
  orderqty integer
  revenue double
}


Ref: fct_sales.order_status_key < dim_order_status.order_status_key
Ref: fct_sales.ship_address_key < dim_address.addressid
Ref: fct_sales.customer_key < dim_customer.customerid
Ref: fct_sales.creditcard_key < dim_credit_card.creditcardid
Ref: fct_sales.product_key < dim_product.productid
Ref: fct_sales.order_date_key < dim_date2.date_key
