var options = {
      "key": "rzp_test_pxJNNIHcr3CxZ6",
      "amount": "{{price.total}}", 
      "currency": "INR",
      "name": "FoodHub",
      "description": "Test Transaction",
      "image": "/static/images/bg-3.jpg",
      "order_id": "{{payment.id}}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
      "handler": function (response){
          var paymentId = response.razorpay_payment_id;
          window.location.href="{% url 'success' %}?order_id={{payment.id}}&amount={{totals.food__price__sum}}&payment_id="+paymentId
      },
      "theme": {
        "color": "#36454F"
      }
  };
  var rzp1 = new Razorpay(options);
  rzp1.on('payment.failed', function (response){
          alert(response.error.code);
          alert(response.error.description);
          alert(response.error.source);
          alert(response.error.step);
          alert(response.error.reason);
          alert(response.error.metadata.order_id);
          alert(response.error.metadata.payment_id);
  });
  document.getElementById('rzp-button1').onclick = function(e){
      rzp1.open();
      e.preventDefault();
  }
