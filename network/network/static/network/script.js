// Like/Unlike button
var like_button = document.querySelectorAll('.like-input');
like_button.forEach(el => {
    let actions = el.value.split(",", 3);
    el.parentElement.addEventListener('click', () => {
        like(parseInt(actions[0]), parseInt(actions[1]), parseInt(actions[2]));
        (actions[0] == 1) ? actions[0] = 0 : actions[0] = 1;
    })
})


// Like/Dislike
function like(action, post_id, user_id) {
    fetch('/like', {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            post_id: post_id,
            user_id: user_id,
            action: (action == 0)? 'like' : 'unlike'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        currentCount = parseInt(document.querySelector(`#like-count-${post_id}-${user_id}`).innerHTML);
        if (action == 0) {
            document.querySelector(`#input-${post_id}-${user_id}`).value = `1,${post_id},${user_id}`;
            document.querySelector(`#like-button-${post_id}-${user_id}`).value = 1;
            document.querySelector(`#like-button-${post_id}-${user_id}`).src = "https://img.icons8.com/fluent/48/000000/hearts.png";
            document.querySelector(`#like-count-${post_id}-${user_id}`).innerHTML = currentCount + 1;
        }
        else {
            document.querySelector(`#input-${post_id}-${user_id}`).value = `0,${post_id},${user_id}`;
            document.querySelector(`#like-button-${post_id}-${user_id}`).value = 0;
            document.querySelector(`#like-button-${post_id}-${user_id}`).src = "https://img.icons8.com/windows/32/000000/like.png";
            document.querySelector(`#like-count-${post_id}-${user_id}`).innerHTML = currentCount - 1;
        }
        
    })
};

// Return selected post and expose edit form
function getPost(post_id) {
    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector(`#post-body-${post_id}`).style.display = 'none';
        document.querySelector(`#edit-form-${post_id}`).style.display = 'block';
        document.querySelector(`#edit-form-body-${post_id}`).value = data.body;
        document.querySelector(`#post-${post_id}`).scrollIntoView({block: 'center', behavior: 'smooth'});
    })
};


// Save post changes
function saveEdit(post_id) {
    let post_body = document.querySelector(`#edit-form-body-${post_id}`).value;
    fetch(`/change`, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            post_id: post_id,
            post_body: post_body
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector(`#post-body-${post_id}`).innerHTML = data.body;
        document.querySelector(`#post-body-${post_id}`).style.display = 'block';
        document.querySelector(`#edit-form-${post_id}`).style.display = 'none';
    })
};

function changeCursor(hover) {
    if (hover === true)
      document.querySelector('body').style.cursor = 'pointer';
    else
      document.querySelector('body').style.cursor = 'default';
};


// Fix csrf_token issue
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

//
//headers: {
//   "X-CSRFToken": getCookie("csrftoken")
//}
