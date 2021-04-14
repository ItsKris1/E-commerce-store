var hideable_billing_form = $('.hideable_billing_form');
var hideable_shipping_form = $('.hideable_shipping_form');

var use_default_billing = document.querySelector("input[name=use_default_billing]");
var use_default_shipping = document.querySelector("input[name=use_default_shipping]");

use_default_shipping.addEventListener('change', function() {
if (this.checked) {
   hideable_shipping_form.hide();
    } else {
     hideable_shipping_form.show();
    }
   })

use_default_billing.addEventListener('change', function() {
   if (this.checked) {
      hideable_billing_form.hide();
    } else {
      hideable_billing_form.show();
    }
   })

