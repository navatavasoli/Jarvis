import json
import re
import requests
import requests.exceptions
from colorama import Fore
from plugin import alias, plugin, require


@alias('geocoder')
@require(network=True)
@plugin('geocode')
class Geocoder:
    jarvis = None
    input_addr = None
    cleaned_addr = None
    help_prompt = ("Geocoding converts street addresses to geographic"
        " latitude and longitude. To use this tool, you can enter a"
        " street address in this form: STREET NUMBER STREET NAME, CITY,"
        " STATE, ZIP. For example: 1000 Main Street, Los Angeles, CA,"
        " 90012. Currently, this tool only works for addresses in the"
        " United States.")

    def __call__(self, jarvis, s):
        """Run the geocoding tool by getting an address from the user, passing
        it to the geocoding API, and displaying the result.

        Parameters
        ----------
        jarvis : CmdInterpreter.JarvisAPI
            An instance of Jarvis that will be used to interact with the user
        s : str
            The input string that was submitted when the plugin was launched.
            Likely to be empty. 
        """
        self.jarvis = jarvis
        self.input_addr = self.get_input_addr(s)
        self.cleaned_addr = self.clean_addr(self.input_addr)
        req = self.get_request()

        # Request failed
        if not req:
            self.jarvis.say("The geocoding service appears to be unavailable."
                " Please try again later.", Fore.RED)
        
        # Request succeeded
        else:
            output = self.parse_request(req)

            if output:
                for result in output:
                    self.jarvis.say("{}: {}".format(result, 
                        output[result]), 
                        Fore.CYAN)

            else:
                self.jarvis.say("No matching addresses found.", Fore.RED)
    
    def parse_request(self, req):
        """Parse a request returned by the geocoding API to extract all
        relevant geocoding data

        Parameters
        ----------
        req : request.Request
            The Request object returned by the geocoding API for an address
            search

        Returns:
        -------
        dict of str: str
            A dictionary of geocoding results for the best matched address
            from the request
        """
        data = json.loads(req.text)
        matches = data['result']['addressMatches']
        
        if matches:
            best_match = matches[0]

            output = {'Address matched': best_match['matchedAddress'],
                    'Latitude': str(best_match['coordinates']['y']),
                    'Longitude': str(best_match['coordinates']['x'])}

        else:
            output = None

        return output

    @property
    def url(self):
        """Format a url to access the geocoding API by combining the cleaned
        input address with the API url.

        Returns:
        -------
        str
            URL to geocode the input address 
        """
        return ("https://geocoding.geo.census.gov/geocoder/locations/"
            "onelineaddress?address={}&benchmark=Public_AR_Current&format="
            "json".format(self.cleaned_addr))

    def get_input_addr(self, s):
        """Get an input address from the user and handle help commands

        Parameters
        ----------
        s : str
            The input string that was submitted when the plugin was launched.
            Likely to be empty. 

        Returns:
        -------
        str
            A street address (unvalidated)
        """
        while True:
            if not s:
                s = self.jarvis.input("Enter the full street address to"
                    " geocode (or type help for options): ") 

            if s.lower() == 'help':
                self.help()
                s = None
            else:
                return s.lower()

    def help(self):
        """Print the help prompt for the plugin"""
        self.jarvis.say(self.help_prompt, Fore.BLUE)

    def clean_addr(self, s):
        """Reformat a string to be URL friendly

        Parameters
        ----------
        s : str
            A street address (unvalidated)

        Returns:
        -------
        str
            The street address with all special characters removed and
            whitespace replaced with +
        """
        # Remove everything that isn't alphanumeric or whitespace
        s = re.sub(r"[^\w\s]", '', s)

        # Replace all whitespace
        s = re.sub(r"\s+", '+', s)

        return s

    def get_request(self):
        """Make a request to the geocoding API and return the request 
        if it succeeds

        Returns:
        -------
        requests.Request
            A request object returned by the API. If any errors were
            encountered during the request, the return will be None.
        """
        try:
            req = requests.get(self.url)
            # Raise HTTPErrors if encountered
            req.raise_for_status()
            return req
        except (requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, 
            requests.exceptions.HTTPError):
            return None
