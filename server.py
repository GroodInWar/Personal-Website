from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus


def submission_to_table(form_data: dict[str, str]) -> str:
    """
    TODO: Takes a dictionary of form parameters and returns an HTML table row

    An example form_data dictionary might look like:
    {
     'name': 'Ryan Hill',
     'location': '2-209 Keller Hall; 200 Union Street SE; Minneapolis, MN 55455',
     'contactInformation': 'Favorite TA',
     'email': 'hill1886@umn.edu',
     'website': 'https://canvas.umn.edu/courses/460624',
    }
    """
    return ("""
<tr>
    <td>"""+form_data["name"]+"""</td>
    <td>"""+form_data["location"]+"""</td>
    <td>"""+form_data["contactInformation"]+"""</td>
    <td>"""+form_data["email"]+"""</td>
    <td>"""+form_data["website"]+"""</td>
</tr>
""")


# NOTE: Please read the updated function carefully, as it has changed from the
# version in the previous homework. It has important information in comments
# which will help you complete this assignment.
def handle_request(url: str, form_data: dict[str, str] | None):
    """
    The url parameter is a *PARTIAL* URL of type string that contains the path
    name and query string.

    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/add-contact.html?name=joe#id=someElement` then the `url` parameter will have
    the value "/add-contact.html?name=joe#id=someElement"

    This function should return two strings in a list or tuple. The first is the
    content to return, and the second is the content-type.
    """

    # Get rid of any query string parameters and fragments
    url, *_ = url.split("?", 1)
    url, *_ = url.split("#", 1)

    # HTML
    if url == "/mycontacts.html":
        return open("static/html/mycontacts.html").read(), "text/html"
    if url == "/add-contact.html":
        return open("static/html/add-contact.html").read(), "text/html"
    elif url == "/aboutme.html" or url == "/":
        return open("static/html/aboutme.html").read(), "text/html"
    elif url == "/added-contacts.html":
        return open("static/html/added-contacts.html").read(), "text/html"
    
    # NOTE: These files may be different for your server, but we include them to
    # show you examples of how yours may look. You may need to change the paths
    # to match the files you want to serve. Before you do that, make sure you
    # understand what the code is doing, specifically with the MIME types and
    # opening some files in binary mode, i.e. `open(..., "br")`.
    # CSS
    elif url == "/css/styles404.css":
        return open("static/css/styles404.css").read(), "text/css"
    elif url == "/css/stylesAboutMe.css":
        return open("static/css/stylesAboutMe.css").read(), "text/css"
    elif url == "/css/stylesAddContact.css":
        return open("static/css/stylesAddContact.css").read(), "text/css"
    elif url == "/css/stylesAddedContacts.css":
        return open("static/css/stylesAddedContacts.css").read(), "text/css"
    elif url == "/css/stylesMyContacts.css":
        return open("static/css/stylesMyContacts.css").read(), "text/css"
    
    # JS
    elif url == "/js/script404.js":
        return open("static/js/script404.js").read(), "text/javascript"
    elif url == "/js/scriptAboutMe.js":
        return open("static/js/scriptAboutMe.js").read(), "text/javascript"
    elif url == "/js/scriptAddContact.js":
        return open("static/js/scriptAddContact.js").read(), "text/javascript"
    elif url == "/js/scriptAddedContacts.js":
        return open("static/js/scriptAddedContacts.js").read(), "text/javascript"
    elif url == "/js/scriptMyContacts.js":
        return open("static/js/scriptMyContacts.js").read(), "text/javascript"
    
    # XML
    elif url == "/xml/contacts.xml":
        return open("static/xml/contacts.xml").read(), "application/xml"
    
    # IMGS
    elif url == "/img/picture1.jpeg":
        return open("static/img/picture1.jpeg", "br").read(), "image/jpeg"
    elif url == "/img/amIcon.jpg":
        return open("static/img/amIcon.jpg", "br").read(), "image/jpg"
    # TODO: Add update the HTML below to match your other pages and implement `submission_to_table`
    
    else:
        return open("static/html/404.html").read(), "text/html; charset=utf-8"


# You shouldn't need to change content below this. It would be best if you just left it alone.

def get_body_params(body: str) -> dict[str, str]:
    if not body:
        return {}

    parameters = body.split("&")

    # Split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # Return a dictionary of the parameters
    return body_dict


class RequestHandler(BaseHTTPRequestHandler):
    def __c_read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body = str(body, encoding="utf-8")
        return body

    def __c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(message)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)

    # noinspection PyPep8Naming
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = handle_request(self.path, None)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )

    # noinspection PyPep8Naming
    def do_POST(self):
        message, content_type = handle_request(self.path, get_body_params(self.__c_read_body()))

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )


def main():
    port = 4131
    print(f"Starting server http://localhost:{port}/")
    httpd = HTTPServer(("", port),
                       lambda request, client_address, server: RequestHandler(request, client_address, server))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
