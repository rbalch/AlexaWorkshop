
class BaseAlexaRequest(object):

    @property
    def intent(self):
        return self.event['request']['intent']

    @property
    def intentName(self):
        return self.event['request']['intent']['name']

    @property
    def intentType(self):
        return self.event['request']['type']

    def __init__(self, event, context):
        self.event = event
        self.context = context

    def buildResponse(self, speechletResponse, sessionAttributes=None):
        if sessionAttributes is None:
            sessionAttributes = {}
        return dict(
            version='1.0',
            sessionAttributes=sessionAttributes,
            response=speechletResponse,
        )

    def buildSpeechletResponse(self, title, responseText, repromptText=None):
        output = dict(
            outputSpeech=dict(
                type='PlainText',
                text=responseText,
            ),
            card=dict(
                type='Simple',
                title=title,
                content=responseText,
            ),
            shouldEndSession=True,
        )
        if repromptText is not None:
            output['reprompt'] = dict(
                outputSpeech=dict(
                    type='PlainText',
                    text=repromptText,
                )
            )
            output['shouldEndSession'] = False
        return output

    def getSlot(self, name):
        return self.intent['slots'][name]['value']

    def response(self):
        if self.intentType == 'IntentRequest':
            return getattr(self, self.intentName)
        return 'intentType: {s.intentType}, intentName: {s.intentName}'.format(s=self)


class MyAlexaRequest(BaseAlexaRequest):

    @property
    def HowAreYouIntent(self):
        return self.buildResponse(
            speechletResponse=self.buildSpeechletResponse(
                title='HowAreYou',
                responseText='i am fine thanks',
            )
        )

    @property
    def MyNameIsIntent(self):
        return self.buildResponse(
            speechletResponse=self.buildSpeechletResponse(
                title='MyNameIsIntent',
                responseText='your name is {name}'.format(name=self.getSlot(name='myName'))
            )
        )

    @property
    def StateRequestIntent(self):
        return self.buildResponse(
            speechletResponse=self.buildSpeechletResponse(
                title='StateRequestIntent',
                responseText='you picked {state}'.format(state=self.getSlot(name='usstate'))
            )
        )


def lambda_handler(event, context):
    return MyAlexaRequest(event=event, context=context).response()
