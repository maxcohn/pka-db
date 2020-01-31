


// once content is loaded
document.addEventListener('DOMContentLoaded', () => {
    
    
    // on search button click
    document.querySelector('#search-button').onclick = () => {
        switch (document.querySelector('#search-type').value) {
            //TODO populate this for real
            case 'episode-pka':
                
                window.open(`/pka/${document.querySelector('#search-box').value}`, '_self');
                break;
            case 'episode-pkn':
                //window.open()
                break;
            case 'guest':

                break;
            case 'event':
                break;
            
            default:
                
        }
        alert()
    }
});

