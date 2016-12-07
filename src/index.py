
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

    def __init__(self, event):
        self.event = event
        self.sessionAttributes = self.event['session']['attributes']

    def buildResponse(self, speechletResponse):
        return dict(
            version='1.0',
            sessionAttributes=self.sessionAttributes,
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
        name = self.getSlot(name='myName')
        self.sessionAttributes['myName'] = name
        return self.buildResponse(
            speechletResponse=self.buildSpeechletResponse(
                title='MyNameIsIntent',
                responseText='your name is {name}'.format(name=name)
            )
        )

    @property
    def StateRequestIntent(self):
        state = self.getSlot(name='usstate')
        states = self.sessionAttributes.get('states', None)
        if states is None:
            self.sessionAttributes['states'] = [state]
        elif state not in states:
            self.sessionAttributes['states'].append(state)

        return self.buildResponse(
            speechletResponse=self.buildSpeechletResponse(
                title='StateRequestIntent',
                responseText='you picked {state}'.format(state=self.getSlot(name='usstate'))
            )
        )


def lambda_handler(event, context):
    return MyAlexaRequest(event=event).response()
