function showLoader() {
        document.getElementById('loader').style.display = 'flex';
        setTimeout(function() {
            document.getElementById('loader').style.display = 'none';
        }, 10000);
    }