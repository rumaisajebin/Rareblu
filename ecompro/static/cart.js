// cart.js

$(document).ready(function() {
    $(".increment-btn").click(function(e) {
        e.preventDefault();
        var productId = $(this).data("product-id");
        updateCart(productId, 'increment');
    });

    $(".decrement-btn").click(function(e) {
        e.preventDefault();
        var productId = $(this).data("product-id");
        updateCart(productId, 'decrement');
    });

    function updateCart(productId, action) {
        $.ajax({
            url: '/update_cart/' + productId + '/' + action + '/',
            method: 'GET',
            success: function(data) {
                // Update the quantity and total price in the UI
                var itemSelector = '#cart-item-' + productId;
                var quantityElement = $(itemSelector).find('.quantity');
                var totalPriceElement = $(itemSelector).find('.text-secondary');
                
                // Assuming the response contains updated quantity and total price
                quantityElement.text(data.quantity);
                totalPriceElement.text('$' + data.total_price);
            },
            error: function(error) {
                // Handle error
            }
        });
    }
});
