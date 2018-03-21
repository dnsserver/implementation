Project
=====

Init
----

```
virtualenv .
source bin/activate
pip install -e .
bin/flask initdb
python wsgi.py
```


Test
----

```
source bin/activate
cd tests
pytest
```

Frontend
--------

```
cd opfrontend
npm run build
```

Remember
--------

1. Register a client on OIDC with introspection rights.
2. In order for flask_admin to work, do: `pip install --upgrade git+https://github.com/flask-admin/flask-admin`
