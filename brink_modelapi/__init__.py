from brink.urls import GET, POST, PUT, DELETE, WS
from brink.decorators import require_request_model


class ModelAPI(object):

    def __init__(self):
        self.endpoints = []

    def __get_url(self, operation, name):
        if operation in ["list", "create"]:
            return "/%s" % name
        else:
            return "/%s/{id}" % name

    def register(self, name, model, operations=["list", "detail"]):
        self.endpoints.append((name, model, operations))

    @property
    def urls(self):
        urls = []

        for (name, model, operations) in self.endpoints:
            for operation in operations:
                try:
                    urls.append(getattr(self, operation)(name, model))
                except AttributeError:
                    raise Exception("Invalid operation `%s`" % operation)

        return urls

    def detail_result(self, name, model_instance):
        return {
            "meta": {
                "detail_url": "/%s/%s" % (name, model_instance.id)
            },
            "data": model_instance
        }

    def collection_result(self, name, model_collection, count, offset, limit):
        return {
            "meta": {
                "count": count,
                "offset": offset,
                "limit": limit
            },
            "data": [self.detail_result(name, ins)
                     for ins in model_collection]
        }

    def list(self, name, model):
        async def handler(request):
            query = request.url.query
            offset = int(query.get("offset", 0))
            limit = int(query.get("limit", 10))
            data = await model.all().slice(offset, offset + limit).as_list()
            count = await model.all().count()
            return 200, self.collection_result(
                name, data, count, offset, limit)
        return GET("/%s" % name, handler)

    def detail(self, name, model):
        async def handler(request):
            id = request.match_info["id"]
            data = await model.get(id)
            return 200, self.detail_result(name, data)
        return GET("/%s/{id}" % name, handler)

    def create(self, name, model):
        @require_request_model(model)
        async def handler(request, model_instance):
            await model_instance.save()
            return 201, self.detail_result(name, model_instance)
        return POST("/%s" % name, handler)

    def update(self, name, model):
        @require_request_model(model)
        async def handler(request, model_instance):
            id = request.match_info["id"]
            model_instance.id = id
            await model_instance.save()
            return 200, self.detail_result(name, model_instance)
        return PUT("/%s/{id}" % name, handler)

    def delete(self, name, model):
        async def handler(request):
            id = request.match_info["id"]
            await model.get(id).delete()
            return 204, None
        return DELETE("/%s/{id}" % name, handler)
