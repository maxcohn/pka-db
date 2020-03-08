


// once content is loaded
document.addEventListener('DOMContentLoaded', () => {
    
    // on press 'enter' to act as submit search button
    document.querySelector('#search-box').onkeyup = (event) => {
        if (event.keyCode == 13) {
            document.querySelector('#search-button').click();
        }
    } 
    
    // on search button click
    document.querySelector('#search-button').onclick = () => {
        let searchType = document.querySelector('#search-type').value;
        let searchText = document.querySelector('#search-box').value;

        if (searchText.trim() === '')
            return;
        switch (searchType) {
            //TODO populate this for real
            case 'episode-pka':
                if (Number.isNaN(parseInt(searchText))) {
                    alert('Please enter a number')
                    break;
                }
                window.open(`/pka/${searchText}`, '_self');
                break;
            case 'episode-pkn':
                if (Number.isNaN(parseInt(searchText))) {
                    alert('Please enter a number')
                    break;
                }
                window.open(`/pkn/${searchText}`, '_self');
                break;
            case 'guest':
                window.open(`/guest/search/${searchText}`, '_self');
                break;
            case 'event':
                window.open(`/event/search/${searchText}`, '_self');
                break;
            
            default:
                
        }
    }

    //TODO: maybe put this in its own script (new-event.js)
    document.querySelector('#submit-event').onclick = async (e) => {
        let show = document.querySelector('#show-input').value;
        let episode = document.querySelector('#episode-input').value;
        let timestamp = document.querySelector('#timestamp-input').value.trim();
        let description = document.querySelector('#description-input').value.trim();
        
        // check if timestamp input is a valid format
        if (!timestamp.match(/^0\d:[0-5]\d:[0-5]\d$/)) {
            alert('Please enter a valid timestamp (format: hh:mm:ss)');
            return;
        }

        // check if episode is valid
        if (episode < 0) {
            alert('Please enter a valid episode number');
            return;
        }

        // check if description is valid
        if (description.trim().length < 5) {
            alert('Please enter a valid description');
            return;
        }


        
        // parse timestamp in hours, minutes, seconds
        let [hours, minutes, seconds] = timestamp.split(':').map(t => parseInt(t, 10));
        let tsSeconds = (hours * 60 * 60) + (minutes * 60) + seconds;

        await fetch('/new-event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                show,
                episode,
                timestamp: tsSeconds,
                description,
            }),
        });
        window.open('/', '_self');
    }

});

