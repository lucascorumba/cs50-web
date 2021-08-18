document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Add functionality to 'send mail' button
  document.querySelector('#submit').addEventListener('click', sendMail);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Populate page
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {
    for (let row = 0; row < data.length; row++) {
      addEmail(data, row);
    };
    console.log(data);
  });

  // Add email to view
  function addEmail(email, row) {
    // Set array with data to be shown
    let cols = [];
    if (mailbox === 'sent') 
      cols.push(email[row].recipients, email[row].subject, email[row].timestamp);
    else 
      cols.push(email[row].sender, email[row].subject, email[row].timestamp);
    // Create div for email box
    const element = document.createElement('div');
    element.setAttribute('id', `email-box${row}`);
    element.setAttribute('onmouseover', 'changeCursor(true)');
    element.setAttribute('onmouseout', 'changeCursor(false)');
    element.className = 'row';
    // Change background on whether email is read/unread
    if (email[row].read === true)
      element.style = 'background-color: white;';
    else
      element.style = 'background-color: #beb8b8;';
    // Append element and add event listeners
    document.querySelector('#emails-view').append(element);    
    document.querySelector(`#email-box${row}`).addEventListener('click', () => seeMail(email[row].id));
    // Add sections inside email box's div
    cols.forEach(el => {
      let temp = document.createElement('div');
      temp.className = 'col';
      temp.innerHTML = `${el}`;
      document.querySelector(`#email-box${row}`).appendChild(temp);
    });
    // Create archive/unarchive button and add event listener to it
    if (mailbox === 'sent')
      return
    else {
      let button = document.createElement('div');
      button.className = 'col-1';
      let buttonValue = (mailbox === 'archive') ? "Unarchive" : "Archive";
      button.innerHTML = `<button class="archive btn btn-dark btn-sm">${buttonValue}</button>`;
      button.addEventListener('click', event => {archiveMail(email[row].id, mailbox); event.stopPropagation();}, true);
      document.querySelector(`#email-box${row}`).appendChild(button);
    };   
  }
}

// View single email
function seeMail(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(data => {
    // Remove elements placed in previous calls, if any
    let content = document.querySelector('#single-view');
    while (content.firstChild)
      content.removeChild(content.firstChild);
    // Show email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#single-view').style.display = 'block';
    // Display data
    const info = document.createElement('div');
    info.setAttribute('id', 'email-info');
    info.className = 'font';
    info.innerHTML = `<b>From:</b> ${data.sender}<br><b>To:</b> ${data.recipients}<br><b>Subject:</b> 
    ${data.subject}<br><b>Timestamp:</b> ${data.timestamp}<br>`;
    document.querySelector('#single-view').append(info);
    const body = document.createElement('div');
    body.setAttribute('id', 'email-body');
    body.className = 'font';
    body.innerHTML = `<hr>${data.body}`;
    document.querySelector('#single-view').append(body);
    // Reply button
    const reply = document.createElement('button');
    reply.className = 'e-view-btn btn btn-sm btn-outline-primary';
    reply.innerHTML = 'Reply';
    reply.addEventListener('click', () => replyMail(data));
    document.querySelector('#email-info').append(reply);
    // Archive button
    const archive = document.createElement('button');
    archive.className = 'e-view-btn btn btn-sm btn-outline-primary';
    let buttonValue = (data.archived === true) ? 'Unarchive' : 'Archive';
    archive.innerHTML = `${buttonValue}`;
    archive.addEventListener('click', () => {
      fetch(`/emails/${data.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: (data.archived === true) ? false : true
        })
      });
      load_mailbox('inbox');
    })
    document.querySelector('#email-info').append(archive);
    // Mark as read
    if (data.read === false) {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }else {};       
  });
}

// Send email
function sendMail() {
  // Get data
  let recipient = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    // Redirects to 'sent 'page
    load_mailbox('sent');
  });
}

// Change cursor when hovering email box
function changeCursor(hover) {
  if (hover === true)
    document.querySelector('body').style.cursor = 'pointer';
  else
    document.querySelector('body').style.cursor = 'default';
}

// Archive/unarchive email
function archiveMail(id, source) {  
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: (source === 'inbox') ? true : false
    })
  });
  load_mailbox(source);
}

// Reply email
function replyMail(data) {
  console.log(data);
  compose_email();
  document.querySelector('#compose-recipients').value = `${data.sender}`;
  document.querySelector('#compose-subject').value = `Re: ${data.subject}`;
  document.querySelector('#compose-body').value = `On ${data.timestamp}, ${data.sender} wrote:\n${data.body}`;
}