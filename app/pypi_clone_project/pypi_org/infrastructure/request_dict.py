from flask import Request


class RequestDictionary(dict):
    def __getattr__(self, key):
        return self.get(key)


def create(request: Request, **route_args) -> RequestDictionary:
    data = {
        # these args are ordered in least to highest priority, so, form posts override URL args, etc.
        **request.args,     # the key/value pairs in the URL query string
        **request.headers,  # Header values
        **request.form,     # the key/value pairs in the body, from a form POST
        **route_args        # additional arguments the method access
    }
    return RequestDictionary(data)

