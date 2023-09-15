const apiKey = 'sYgR9T3NJ0nVII4N19oXSRtXn';
const apiSecretKey = 'iba2pj5m5nDo8W77xR5EgrFzguUkQYgM6CdV4cusKnsEp1Hb5h';
const accessToken = '1702459518687604736-wJ9ThIO2bpamJlFc5V16EKCzgxJcZ3';
const accessTokenSecret = 'n8KKIRr0dKJzpB9xji4DAeAAvRlJatLeyIbBAadUmKYXr';

const beartoken = "AAAAAAAAAAAAAAAAAAAAADHWpwEAAAAAGLXBpCjabmnbhjmn94sOTb2gv6o%3D5ZHe2QdjtPL3bt1nSjQlu95VEwkO82sqKJQrNwve4zDTDKYDfm"

function GetAllAccount() {
    const tweetContent = document.getElementById('tweetContent').value;
    const tweetData = { text: tweetContent };

    fetch('https://ads-api.twitter.com/11/accounts', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${beartoken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error creating tweet:', error);
    });
}

function createTweet() {
    //const tweetContent = document.getElementById('tweetContent').value;
    //const tweetData = { text: tweetContent };

    fetch('https://ads-api-sandbox.twitter.com/12/accounts', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${beartoken}`,
            'Content-Type': 'application/json',
        },
        //body: JSON.stringify(tweetData),
    })
    .then(response => {
        response.json();
        console.log(response.status)
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error creating tweet:', error);
    });
}

createTweet()