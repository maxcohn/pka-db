


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
});

