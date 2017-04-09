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
#TODO username
	#error if not valid
#TODO password
	#error if not valid
#TODO verify password
    #clear password for security
    #error message if password doesnt match
#TODO email
    #error if user gives invalid email
#TODO submit
	#redirect/preserve username & email
import webapp2
import cgi
import re
#Given module and functions
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

def build_page(username1, username_error, password_error, verify_password_error,
email1, email_error):
	top = ("<head>"
		"<title>Sign Up</title>"
		"<style type='text/css'>"
			".error {color: red}"
		"</style>"
		"</head>")
#TODO username,password,verify,email form
    #error message if name not valid...has spaces...ect
    #preserve username and email
	header = "<h2>Signup</h2>"
	table = ("<table>"
		"<tr>"
			"<td>Username</td>"
			"<td><input type='text' name='username' value='" + username1 + "' required></input></td>"
			"<td class='error'>" + username_error + "</td>"
		"</tr>"
		"<tr>"
			"<td>Password</td>"
			"<td><input type='password' name='password' required></input></td>"
			"<td class='error'>" + password_error + "</td>"
		"</tr>"
		"<tr>"
			"<td>Verify Password</td>"
			"<td><input type='password' name='verify_password' required></input></td>"
			"<td class='error'>" + verify_password_error + "</td>"
		"</tr>"
		"<tr>"
			"<td>Email (optional)</td>"
			"<td><input type='text' name='email' value='" + email1 + "'></input></td>"
			"<td class='error'>" + email_error + "</td>"
		"</tr>"
	"</table>")

	submit = "<input type='submit'/>"

	form = top + "<form method='post'>" + table + submit + "</form>"

	return form

class MainHandler(webapp2.RequestHandler):
	def get(self):
		content = build_page("", "", "", "", "", "")
		self.response.write(content)
#Post/Loop validity functions
	def post(self):
		errorcount = 0
		username = self.request.get("username")
		username = cgi.escape(username, quote=True)
		password = self.request.get("password")
		verify_password = self.request.get("verify_password")
		email = self.request.get("email")
		email = cgi.escape(email, quote=True)
		username_error = ""
		password_error = ""
		verify_password_error = ""
		email_error = ""
#TODO
#error message if name has spaces
#error message if password 	not valid/doesnt match
#error if user gives email and invalid
		if not username or not valid_username(username):
			username_error = "That's not a valid username"
			errorcount += 1
		if not password or not valid_password(password):
			password_error = "That's not a valid password"
			errorcount += 1
		if password != verify_password:
			verify_password_error = "Passwords don't match"
			errorcount += 1
		#optional
		if email and not valid_email(email):
			email_error = "That's not a valid email"
			errorcount += 1

		if errorcount > 0:
			content = build_page(username, username_error, password_error,
            verify_password_error, email, email_error)
			self.response.write(content)
		else:
			self.redirect("/welcome?username=" + username)
#TODO
#redirect user to welcomepage if fields are valid
class Welcome(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		header = "<h2>Welcome, " + username + "!" + "</h2>"
		self.response.write(header)

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', Welcome)
], debug=True)
