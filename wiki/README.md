# Project 1: Wiki

## Description
This project is one of six needed for approval on the [CS50 Web Programming](https://cs50.harvard.edu/web/2020/) course.

The objective of [wiki project](https://cs50.harvard.edu/web/2020/projects/1/wiki/) was to build a webpage similar in concept to [Wikipedia](https://www.wikipedia.org/), where each encyclopedia route can be viewed by visiting that entry's page. In this project, the entries are stored with *Markdown* language.

## Specification
To achieve completion of the assignment, the following features should be implemented correctly:
* **Entry Page**: Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, render a page that displays the contents of that encyclopedia entry.
	* If an entry that does not exist is requested, the user is presented with an error page indicating that their request page was not found.
* **Index Page**: The user can click on any entry name to be taken directly to that entry page.
* **Search**: The user can type in a query to a search box in the sidebar to look for an encyclopedia entry.
	* If the query matches the name of an encyclopedia entry, the user is redirected to that entry’s page.
	* If the query does not match the name of an encyclopedia entry, the user is instead taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were `Py`, then `Python` should appear in the search results.
	* Clicking on any of the entry names on the search results page takes the user to that entry’s page.
* **New Page**: Clicking “Create New Page” in the sidebar takes the user to a page where they can create a new encyclopedia entry.
	* Users are able to enter a title for the page and, in a `textarea`, and enter the Markdown content for the page.
	* Users are able to click a button to save their new page.
	* When the page is saved, if an encyclopedia entry already exists with the provided title, the user is presented with an error message.
	* Otherwise, the encyclopedia entry is saved to disk, and the user is taken to the new entry’s page.
* **Edit Page**: On each entry page, the user is able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a `textarea`.
	* The `textarea` is pre-populated with the existing Markdown content of the page. (i.e., the existing content is the initial value of the `textarea`).
	* The user is able to click a button to save the changes made to the entry.
	* Once the entry is saved, the user is redirected back to that entry’s page.
* **Random Page**: Clicking “Random Page” in the sidebar takes the user to a random encyclopedia entry.
* **Markdown to HTML Conversion**:  On each entry’s page, any Markdown content in the entry file is converted to HTML before being displayed to the user.

The full demonstration of these features can be seen in this [video](https://youtu.be/aTD2NrHtEEI). Each one of them is marked in a *timestamp*.

## Usage
To build up the local development server execute the command:
```py
python3 manage.py runserver
```
