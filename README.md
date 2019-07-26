# reward
A simple python-based service to create vouchers or users based on value and mark vouchers as used or expired.

# Endpoints

## Create vouchers
```POST /vouchers```

Accepts a list of customers and creates vouchers for each. Will not create voucher for a customer if the customer alreday has one.
### Payload
10, Dayo, 10000
122, Femi, 2000
35, Akin Alabi, 4500
41, Salami, 8700,
194, Belle Man, 13000
328, Santi, 2300
81, Ibro, 4000

## Activate a voucher
``` POST /vouchers/<customer_id>/customer-id```

### Response
```
{
    "amount": 500.0,
    "code": "TKDV0003",
    "expires": "2019-07-31 07:07:59",
    "is_useable": true
}
```

When a voucher is activated for a customer, the expiry date is set

## Fetch a voucher
### Request
``` GET /vouchers/<code>```
### Response
```
{
    "amount": 500.0,
    "code": "TKDV0003",
    "expires": "2019-07-31 07:07:59",
    "is_useable": true
}
```
  
Sets a voucher as used and unusable in the future



## Mark voucher as used
``` PUT /vouchers/<code>```
### Response
```
{
    "amount": 500.0,
    "code": "TKDV0003",
    "expires": "2019-07-31 07:07:59",
    "is_useable": false
}
```
Sets a voucher as used and unusable in the future
