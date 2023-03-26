# bondable

API for bondable

To run:

```
$ docker-compose up
```

Browse at http://localhost:8000/swagger

Changelog:
1. AppLog added

$ az acr login --name bondableregistry
$ docker build . -t bondableregistry.azurecr.io/bondable:1.0
$ docker push bondableregistry.azurecr.io/bondable:1.0