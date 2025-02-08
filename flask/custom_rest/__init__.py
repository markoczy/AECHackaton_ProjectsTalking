"""This is the custom flask package of BORM.

Define the custom REST endpoints in this package, import them here and add it into the `app_blueprints` list.

For example, if you have defined new endpoints (Flask Blueprint) for url "/tests", you can do following:

```python
from custom_rest.tests.tests import tests_app
app_blueprints = [(tests_app, '/tests')]
```

See documentation of Flask Blueprint at https://flask.palletsprojects.com/en/2.0.x/blueprints/
"""

# API-Key: N9MKRMxO1F4iuoCPIAaBMcaROQS4gDHWCs5NYm7Gaiz

# A list of tuples (Blueprint, url_prefix)
from custom_rest.projects_talking.endpoints import api as projects_talking
app_blueprints = [(projects_talking, '/projects_talking')]
