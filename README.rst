Mixpanel, Inc. -- http://mixpanel.com/

Python API client library to consume mixpanel.com analytics data.


mixpanel_export
===============

Mixpanel exporter based on the code written here: 
https://mixpanel.com/site_media//api/v2/mixpanel.py

Initialization
--------------
- An example of initializing the exporter follows::

  from mixpanel_export import Exporter
  exporter = Exporter("my-api-key", "my-api-secret")
  
- All other options are detailed at `Mixpanel.com's Export API Documentation:
  <https://mixpanel.com/docs/api-documentation/data-export-api>`_.


Access Example
--------------
One example (drawn from Mixpanel's documentation) is to "Get the top values
for a property". Here is an example of how you would execute this request::

  methods = ['events', 'properties', 'values']
  params = { 'event': 'splash features',
             'interval': '7',
             'name': 'feature',
             'type': 'general',
             'unit': 'day' }
  result = exporter.export(methods, params)
            
To get bulk data, you'd issue the following command::

  params = {
      'from_date': datetime.strptime("2013-01-01", "%Y-%m-%d"),
      'to_date': datetime.strptime("2013-09-01", "%Y-%m-%d")
  }
  result = exporter.export_raw(params)

Additional
----------
- For more information, visit `Mixpanel's Export API Documentation 
  <https://mixpanel.com/docs/api-documentation/data-export-api>`_.
