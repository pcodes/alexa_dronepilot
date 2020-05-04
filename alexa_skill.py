import sys
from v9 import V9Component

def handle_skill_endpoint(http_method, path, request_arguments, request_body):
    print(http_method, path, request_arguments, request_body)
    return 200, "All good here"


if __name__ == '__main__':
    print("Arguments " + str(sys.argv))
    comp = V9Component(sys.argv[1], sys.argv[2])

    comp.register_operation("dronepilot", handle_skill_endpoint)

    comp.loop()
