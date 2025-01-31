const paymentDetails = document.getElementById("payment_set");
const addressDetails = document.getElementById("address_set");

if (paymentDetails !== null && addressDetails !== null) {
    document.write("<a href='/order-confirmation'><button class='btn btn-outline-primary btn-lg'>Confirm payment</button></a>");
} else {
    document.write("<h4 class='text-secondary'>Enter payment and address details</h4>")
}