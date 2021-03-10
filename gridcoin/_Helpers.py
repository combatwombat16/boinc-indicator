import types


def clean_dict(in_dict):
    resp_json = in_dict
    for key in list(resp_json.keys()):
        if not isinstance(key, str):
            continue
        value = resp_json[key]
        del resp_json[key]
        resp_json[key.replace("-", "_").replace(" ", "_")] = value
    return resp_json
