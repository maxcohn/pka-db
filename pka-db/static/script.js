


// once content is loaded
document.addEventListener('DOMContentLoaded', () => {
    
    
    // on search button click
    document.querySelector('#search-button').onclick = () => {
        let searchType = document.querySelector('#search-type').value;
        let searchText = document.querySelector('#search-box').value;

        if (searchText.trim() === '')
            return;
        switch (searchType) {
            //TODO populate this for real
            case 'episode-pka':
                
                window.open(`/pka/${searchText}`, '_self');
                break;
            case 'episode-pkn':
                window.open(`/pkn/${searchText}`, '_self');
                break;
            case 'guest':
                window.open(`/guest/search/${searchText}`, '_self');
                break;
            case 'event':
                break;
            
            default:
                
        }
    }
});

