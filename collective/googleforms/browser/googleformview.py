from BeautifulSoup import BeautifulSoup
import urllib
import urlparse
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.googleforms import googleformsMessageFactory as _

HTMLFIELD=u"""<div class="field">
          <span></span>
          <label class="formQuestion">%(title)s</label>
          %(required)s
          <div class="formHelp" id="title_help">%(description)s</div>
          <div class="fieldErrorBox"></div>
          %(raw)s
        </div>"""

class IGoogleFormView(Interface):
    """
    GoogleForm view interface
    """

    def validate():
        """ validate url"""

    def src():
        """ return the form url ready to be embeded"""

    def form_html():
        """ return form in html """

class GoogleFormView(BrowserView):
    """
    GoogleForm browser view
    """
    implements(IGoogleFormView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.url = context.getRemoteUrl()
        self.parsed = urlparse.urlparse(self.url).params
        self._validated = None
        self._form_key = None
        self.form = None
        self._html = ""
        self._form_structure = None

    def validate(self):
        if self._validated is not None:
            return self._validated
        url = self.url
        parsed = urlparse.urlparse(url)
        https = parsed.scheme == 'https'
        spreadsheets = parsed.hostname == 'spreadsheets.google.com'
        params = dict([part.split('=') for part in parsed.query.split('&')])
        formkey = 'formkey' in params
        self._form_key = params['formkey']
        return https and spreadsheets and formkey

    def form_key(self):
        return self._form_key

    def src(self):
        return "https://spreadsheets.google.com/embeddedform?formkey="+self.form_key()

    def fetch(self):
        if not self._html:
            self._html = urllib.urlopen(self.src())
        return self._html
    
    def form_structure(self):
        if self._form_structure: return self._form_structure
        html = self.fetch()
        form = {'action':'',
                'fields':[]}
        soup = BeautifulSoup(html)
        form['action'] = str(soup.find('form')[u'action'])
        entries = soup.findAll("div",{"class":"ss-form-entry"})

        for entry in entries:
            field = {'title':u'',
                     'description':u'',
                     'type':'',
                     'required':''}
            title = entry.find('label', {'class':'ss-q-title'})
            if title:
                title = title.text
                if title.endswith(u'*'):
                    field['required'] = '*'
                    title = title[:-1]
                field['title'] = title
            description = entry.find('label', {'class':'ss-q-help'})
            if description:
                field['description'] = description.text
            inputs = entry.findAll('input')
            if len(inputs)==0:
                textarea = entry.find('textarea')
                if textarea:
                    field['type']='textarea'
                    field['raw']=textarea
            elif len(inputs) == 1:
                field['type']='input'

                checkbox = entry.find('label',{'class':'ss-choice-label'})
                raw = str(inputs[0])
                if checkbox: 
                     raw += checkbox.text
                field['raw'] = raw
            else:
                field['type']='inputs'
                raw = str(entry.find('ul'))
                field['raw']=raw
            if field['type']:
                form['fields'].append(field)

        self._form_structure = form
        return form

    def form_html(self, mode="within"):
        if mode != "within":
            html = self.fetch()
            return html.body.renderContents()

        structure = self.form_structure()
        fields = structure['fields']
        html = '<input type="hidden" value="%s" name="formkey"/>'%self.form_key()

        for field in fields:
            html+=HTMLFIELD%field

        return html
