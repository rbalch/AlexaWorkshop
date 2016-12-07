# Alexa Workshop

I made this during the workshop to avoid nodejs. This implements the basics for the workshop using aws lambda and Alexa interactions



#### BaseAlexaRequest

Implements the basics you need (processing incoming requests, parsing the incoming variables, and loading/returning the session attributes).

Inherit from it and make a @property for each incoming intent.