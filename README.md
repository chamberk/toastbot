# toastbot
Hack the Gap toast bot

# POST localhost:5000/addPhoneNumber
header: Content-Type : application/json
{
	"name": "Rose",
	"phoneNumber": "0987654321"
}

# GET localhost:5000/phoneNumbers
{
  "phoneNumbers": [
    "1234567890",
    "0987654321"
  ]
}

# GET localhost:5000/allData
{
  "phoneNumbers": [
    {
      "id": 1,
      "name": "Christine",
      "phoneNumber": "1234567890"
    },
    {
      "id": 2,
      "name": "Rose",
      "phoneNumber": "0987654321"
    }
  ]
}

# GET localhost:5000/deletePhoneNumber/1234567890
{
  "status": "deleted successfully"
}
