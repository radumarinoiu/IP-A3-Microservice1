import os
import requests
import json

methods = {
    "get": requests.get,
    "post": requests.post,
    "put": requests.put,
    "delete": requests.delete
}



def parse_input(input):
    method = input["method"]
    if method in methods:
        if "object" in input and input["object"]:
            resp = methods[method](input["url"], input["object"])
        else:
            resp = methods[method](input["url"])
        response = {
            "status_code": resp.status_code,
            "object": resp.json()
        }

        return response
    return None


# Input
# {
#     "method": "",
#     "url": "",
#     "object": {}
# }

# Output
# {
#     "status_code": 200,
#     "object": {}
# }


for test in os.listdir("./tests"):
    with open(os.path.join("./tests", test), "rb") as f:
        test_object = json.load(f)
        tests = test_object

    with open(os.path.join("./output", test), "wb") as f:
        test_output = parse_input(test_object["input"])
        if test_output == test_object["output"]:
            test_result = True
        else:
            test_result = False
        json.dump({
            "result": test_result,
            "expected": tests["output"],
            "got": test_output
        }, f, indent=4)
