import sys
import requests
import json
from v9 import V9Component


def on_launch(launch_request, session):
     return get_welcome_response()

def get_welcome_response():
    session_attributes = {}
    should_end_session = False
    card_title = "Drone Pilot"
    speech_output = "Welcome to the Alexa Drone Pilot skill!" \
                    "You can ask me to send a variety of different commands to your Tello drone. I can have " \
                    "the drone take off or move in a particular direction. "
    reprompt_text = "Please ask me to send the drone a command. Maybe have it take off?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Drone Pilot"
    speech_output = "Thank you for using Drone Pilot!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "TakeOffIntent":
        return drone_takeoff()
    elif intent_name == "LandIntent":
        return drone_land()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def drone_takeoff():
    session_attributes = {}
    card_title = "Drone Taking Off..."
    reprompt_text = ""
    should_end_session = False

    speech_output = "Drone now taking off!"
    requests.post('68.9.94.121:6000/drone/command/takeoff')

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def drone_land():
    session_attributes = {}
    card_title = "Drone Landing..."
    reprompt_text = ""
    should_end_session = False

    speech_output = "Drone now landing!"
    requests.post('68.9.94.121:6000/drone/command/land')

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }

def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
         return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return handle_session_end_request()

def handle_skill_endpoint(http_method, path, request_arguments, request_body):
    body_json = json.loads(request_body)
    print(body_json)
    skill_result = lambda_handler(body_json, body_json["context"])
    print(http_method, path, request_arguments, request_body)
    return 200, skill_result


if __name__ == '__main__':
    print("Arguments " + str(sys.argv))
    comp = V9Component(sys.argv[1], sys.argv[2])

    comp.register_operation("dronepilot", handle_skill_endpoint)

    comp.loop()
