#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type = "text/css">
        .error {
            color: red;
        }
    </style>
</head>

<body>
    <h1>
        <a href = "/">Signup</a>
    </h1>
"""
add_form = """
<form action="/" method = "post">
    <br>
    <br>
    <label>
        User Name:
        <input type = "text" name = "username" value = ""/>
    </label>
        <div style = "color: red">%(error_username)s</div>
    <br>
    <label>
        Password:
        <input type = "password" name = "password" value = ""/>
    </label>
        <div style = "color: red">%(error_password)s</div>
    <br>
    <label>
        Verify Password:
        <input type = "password" name = "verify" value = ""/>
    </label>
        <div style = "color: red">%(error_verify)s</div>
    <br>
    <label>
        Email (optional):
        <input type = "text" name = "email" value = ""/>
    </label?
        <div style = "color: red">%(error_email)s</div>
    <br>
    <br>
    <input type = "submit" value = "Submit"/>

</form>
"""

page_footer = """
</body>
</html>
"""

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return user_re.match(username)

password_re = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password_re.match(password)

email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or email_re.match(email)




class MainHandler(webapp2.RequestHandler):


    def get(self):
        self.write_form()

    def write_form(self, error_username="", error_password="", error_verify="", error_email="", username = "", email=""):
        values = {"error_username":error_username,
            "error_password":error_password,
            "error_verify":error_verify,
            "error_email":error_email,
            "username":username,
            "email":email}
        self.response.out.write(page_header + (add_form % values) + page_footer)

    def post(self):
        have_error = False

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        error_email = ""
        error_username = ""
        error_verify = ""
        error_password = ""

        if not valid_username(username):
            error_username = "Your username is not valid"
            have_error = True

        if not valid_password(password):
            error_password = "Your password is not valid"
            have_error = True

        if password != verify:
            error_verify = "Your passwords do not match"
            have_error = True

        if not valid_email(email):
            error_email = "Your email is not valid"
            have_error = True

        if have_error:
            self.write_form(error_username, error_password, error_verify, error_email, username, email)
        else:
            u = str(username)
            welcome_msg = "Welcome, %s!" % u
            self.response.out.write(welcome_msg)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
