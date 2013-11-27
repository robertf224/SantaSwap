SantaSwap
=========

A web application to quickly create secret santa exchanges.

Description
-----------

The application is written in python using the Flask framework, and can be found live [here](http://fidler.io/SantaSwap/).  Note: this will only work with verified numbers if deployed with a Twilio trial account.  Also, if deployed with a full account, it would make sense to do rate-limiting.

Changes
-------

* Fix jQuery slideDown issue on mobile/tablets.
* Fix spacing issue on mobile (Apparently just making the browser window smaller isn't a good enough testing environment for mobile.  Who knew).