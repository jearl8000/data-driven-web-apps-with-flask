import flask
from werkzeug.datastructures import MultiDict


class RequestDictionary(dict):
    def __init__(self, *args, default_val=None, **kwargs):
        self.default_val = default_val
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self.get(key, self.default_val)


def create(default_val=None, **route_args) -> RequestDictionary:
    request = flask.request

    # Adding this retro actively. Some folks are experiencing issues where they
    # are getting a list rather than plain dict. I think it's from multiple
    # entries in the multidict. This should fix it.
    args = request.args
    if isinstance(request.args, MultiDict):
        args = request.args.to_dict()

    form = request.form
    if isinstance(request.args, MultiDict):
        form = request.form.to_dict()

    data = {
        # these args are ordered in least to highest priority, so, form posts override URL args, etc.
        **args,     # the key/value pairs in the URL query string
        **request.headers,  # Header values
        **form,     # the key/value pairs in the body, from a form POST
        **route_args        # additional arguments the method access
    }
    return RequestDictionary(data, default_val=default_val)

