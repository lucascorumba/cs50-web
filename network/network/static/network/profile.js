// Follow/Unfollow button
document.querySelector('#follow-button').addEventListener('click', () => {
    let action = document.querySelector('#operation').value;
    let profile = document.querySelector('#profile').value;
    let currentUser = document.querySelector('#current-user').value;
    network(action, profile, currentUser);
}) 


// Follow/Unfollow 
function network(action, profile_id, user_id) {
    fetch('/follow', {
        method: (action == 1)? 'DELETE' : 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            profile_id: profile_id,
            user_id: user_id
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        currentFollowers = parseInt(document.querySelector('#followers').innerHTML);
        if (action == 0){
            document.querySelector('#followers').innerHTML = currentFollowers + 1;
            document.querySelector('#follow-button').value = 'Unfollow';
            document.querySelector('#operation').value = 1;
        }
        else {
            document.querySelector('#followers').innerHTML = currentFollowers - 1;
            document.querySelector('#follow-button').value = 'Follow';
            document.querySelector('#operation').value = 0;
        }
    })
};