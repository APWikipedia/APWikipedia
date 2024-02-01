document.getElementById('searchButton').addEventListener('click', function() {
    search('http://localhost:5000/search');
});

document.getElementById('rankedSearchButton').addEventListener('click', function() {
    search('http://localhost:5000/ranked_search');
});

function search(url) {
    var query = document.getElementById('searchQuery').value;
    var results = document.getElementById('searchResults');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (Array.isArray(data.results)) {
            // 保留前50条数据
            var topResults = data.results.slice(0, 50);
        
            results.innerHTML = topResults.map(result => `<div>${result}</div>`).join('');
        } else {
            results.innerHTML = JSON.stringify(data.results, null, 2);
        }        
    })
    .catch(error => {
        console.error('Error:', error);
        results.innerHTML = 'Unxepected Error';
    });
}
