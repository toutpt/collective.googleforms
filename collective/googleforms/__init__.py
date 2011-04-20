  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

googleformsMessageFactory = MessageFactory('collective.googleforms')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
