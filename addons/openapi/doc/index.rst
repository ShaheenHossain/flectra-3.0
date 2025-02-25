==========================
 REST API/Openapi/Swagger
==========================

.. contents::
   :local:

Installation
============

* Install python packages:

  ``python3 -m pip install bravado_core swagger_spec_validator``

* `Install <https://flectra-development.readthedocs.io/en/latest/flectra/usage/install-module.html>`__ this module in a usual way

Configuration
=============

Activating and customization
----------------------------

* Open menu ``[[ OpenAPI ]] >> OpenAPI >> Integrations``
* Click ``[Create]``
* Specify **Name** for integration, e.g. ``test``
* Set **Log requests** to *Full*
* Set **Log responses** to *Full*
* In ``Accessable models`` tab click ``Add an item``

  * Set **Model**, for example *res.users*
  * Configure allowed operations

    * **[x] Create via API**

      * Set **Creation Context Presets**, for example

        * **Name**: ``brussels``
        * **Context**: ``{"default_tz":"Europe/Brussels", "default_lang":"fr_BE"}``

    * **[x] Read via API**

      * Set **Read One Fields** -- fields to return on reading one record
      * Set **Read Many Fields** -- fields to return on reading multiple records

        Note: you can use Export widget in corresponding *Model* to create *Fields list*. To do that:

        * Open menu for the *Model*
        * Switch to list view
        * Select any record
        * click ``[Action] -> Export``
        * Set **Export Type** to *Export all Data*
        * Add the fields you need to right column
        * Click **Save fields list**, choose name and save the list
        * Now the list is availab to set **Read One Fields**, **Read Many Fields** settings

    * **[x] Update via API**
    * **[x] Delete via API**

* Click ``[Save]``
* Copy **Specification Link** to use it in any system that support OpenAPI

Authentication
--------------

* `Activate Developer Mode <https://flectra-development.readthedocs.io/en/latest/flectra/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Users & Companies >> Users``
* Select a user that will be used for iteracting over API
* In **Allowed Integration** select some integrations
* Copy **OpenAPI Token** to use it in any system that support OpenAPI

If necessary, you can reset the token by pressing ``[Reset OpenAPI Token]`` button

Usage
=====

Swagger Editor
--------------
As the simplest example, you can try API in Swagger Editor. It allows to review and check API

* Open http://editor.swagger.io/
* Click menu ``File >> Import URL``
* Set **Specification link**
* RESULT: Specification is parsed succefully and you can see API presentation
* Click ``[Authorize]`` button

  * **Username** -- set database name
  * **Password** -- set **OpenAPI Token** (how to get one is described in `authentication <#authentication>`__ above)

Note:
  The Swagger Editor sends requests directly from browser which leads to CORS error and work with it is not available in `flectra.sh`.
  The easiest solution is to simply copy-past the curl command from Swagger Editor and run it from the terminal.

  Alternatively, you can grant CORS headers in your web server. Below is example for Nginx::

    location /api/v1 {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*' 'always';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, PATCH' 'always';
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' 'always';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
        if ($request_method = 'POST') {
            add_header 'Access-Control-Allow-Origin' '*' 'always';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, PATCH' 'always';
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' 'always';
        }
        if ($request_method = 'GET') {
            add_header 'Access-Control-Allow-Origin' '*' 'always';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, PATCH' 'always';
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' 'always';
        }
        if ($request_method = 'PUT') {
            add_header 'Access-Control-Allow-Origin' '*' 'always';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, PATCH' 'always';
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' 'always';
        }
        if ($request_method = 'DELETE') {
            add_header 'Access-Control-Allow-Origin' '*' 'always';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, PATCH' 'always';
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' 'always';
        }
        if ($request_method = 'PATCH') {
            add_header 'Access-Control-Allow-Origin' '*' 'always';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, PATCH' 'always';
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' 'always';
        }

        # ...
    }

How to call methods with arguments via API
------------------------------------------

Here is an example of calling a search method with domain.

This is how it is usually done from python code:

.. code-block:: python

  partner_ids = self.env["res.partner"].search([("is_company", "=", "True")])

On using API it would be as following:

.. code-block:: bash

  curl -X PATCH "http://example.com/api/v1/demo/res.partner/call/search" -H "accept: application/json" \
  -H "authorization: Basic BASE64_ENCODED_EXPRESSION" -H "Content-Type: application/json" \
  -d '{ "args": [[["is_company", "=", "True" ]]]}'


Updating existing record
-----------------------------

For example, to set *phone* value for a partner, make a PUT request in the following way:

.. code-block:: bash

  curl -X PUT -H "Authorization: Basic BASE64_ENCODED_EXPRESSION" \
  -H "Content-Type: application/json" -H "Accept: */*" \
  -d '{ "phone": "+7123456789"}' "http://example.com/api/v1/demo/res.partner/41"

To set many2one field, you need to pass id as a value:

.. code-block:: bash

  curl -X PUT -H "Authorization: Basic BASE64_ENCODED_EXPRESSION" \
  -H "Content-Type: application/json" -H "Accept: */*" \
  -d '{ "parent_id": *RECORD_ID*}' "http://example.com/api/v1/demo/res.partner/41"

For more examples visit https://itpp.dev/sync website
