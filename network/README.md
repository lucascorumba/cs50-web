# CS50w Hands-on Project - Project 4: Network

## Description
This project is one of six needed for approval on the [CS50 Web Programming](https://cs50.harvard.edu/web/2020/) course.

The objective of [network project](https://cs50.harvard.edu/web/2020/projects/4/network/) was to design a [Twitter](https://twitter.com/)-like social network website for making posts, following other users, and "like" posts.

## Specification
To achieve completion of the assignment, the following features should be implemented correctly:
* **New Post**: Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
* **All Posts**: An “All Posts” link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.
	* Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.
* **Profile Page**: Clicking on a username loads that user’s profile page. This page should:
	* Display the number of followers the user has, as well as the number of people that the user follows.
	* Display all of the posts for that user, in reverse chronological order.
	* For any other user who is signed in, this page also displays a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. This only applies to any “other” user: users are not able to follow themselves.
* **Following**: The “Following” link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
	* This page should behave just as the “All Posts” page does, just with a more limited set of posts.
	* This page is only available to users who are signed in.
* **Pagination**: On any page that displays posts, posts are only displayed in blocks of 10 per page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which are older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.
* **Edit Post**: The user is able to click an “Edit” button or link on any of their own posts to edit that post.
	* When a user clicks “Edit” for one of their own posts, the content of their post is replaced with a `textarea` where the user can edit the content of their post.
	* The user is then able to “Save” the edited post. This must be achieved without requiring a reload of the entire page.
	* For security, ensure that the application is designed such that it is not possible for a user, via any route, to edit another user’s posts.
* **"Like" and "Unlike"**: The user is able to click a button or link on any post to toggle whether or not they “like” that post.
	* This task must be performed asynchronously. The server may be informed to update the like count, then, the post’s like count displayed on the page is updated, without requiring a reload of the entire page.

The full demonstration of these features can be seen in this [video](https://youtu.be/sDaq4ZepyIw). Each one of them is marked in a *timestamp*.

## Usage
To build up the local development server execute the command:
```py
python3 manage.py runserver
```
