# CS50w Hands-on Project - Project 3: Mail

## Description
This project is one of six needed for approval on the [CS50 Web Programming](https://cs50.harvard.edu/web/2020/) course.

The objective of [mail project](https://cs50.harvard.edu/web/2020/projects/3/mail/) was to design a front-end for a single-page-app email client that makes API calls to send and receive emails.

> For this project, the API inside `views.py` was provided by the course staff, and the completion of the project could be achieved by just writing HTML and JavaScript.

## Specification
To achieve completion of the assignment, the following features should be implemented correctly:
* **Send Mail**: When a user submits the email composition form, add JavaScript code to actually send the email.
	* Once the email has been sent, load the user’s sent mailbox.
* **Mailbox**: When a user visits their "Inbox", "Sent" mailbox, or "Archive", load the appropriate mailbox.
	* When a mailbox is visited, the application first query the API for the latest emails in that mailbox.
	* When a mailbox is visited, the name of the mailbox appears at the top of the page.
	* Each email is then be rendered in its own box (e.g. as a `<div>` with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.
	* If the email is unread, it appears with a gray background. If the email has been read, it appears with a white background.
* **View Email**: When a user clicks on an email, the user is taken to a view where they see the content of that email.
	* The application shows the email’s sender, recipients, subject, timestamp, and body.
	* Once the email has been clicked on, the email is marked as read.
* **Archive and Unarchive**: Allow the user to archive and unarchive emails that they have received.
	* When viewing an "Inbox" email, the user is presented with a button that lets them archive the email. When viewing an "Archive" email, the user is presented with a button that lets them unarchive the email. This requirement does not apply to emails in the "Sent" mailbox.
	* Once an email has been archived or unarchived, load the user’s inbox.
* **Reply**: Allow the user to reply to an email.
	* When viewing an email, the user is presented with a “Reply” button that lets them reply to the email.
	* When the user clicks the “Reply” button, they are taken to the email composition form.
	* Pre-fill the composition form with the `recipient` field set to whoever sent the original email.
	* Pre-fill the subject line. If the original email had a `subject` line of `foo`, the new subject line should be `Re: foo`. (If the subject line already begins with `Re: `, no need to add it again.)
	* Pre-fill the body of the email with a line like `"On Jan 1 2020, 12:00 AM foo@example.com wrote:"` followed by the original text of the email.

The full demonstration of these features can be seen in this [video](https://youtu.be/dvKJDwIVU2c). Each one of them is marked in a *timestamp*.

## Usage
To build up the local development server execute the command:
```py
python3 manage.py runserver
```
