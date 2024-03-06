document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('query');
    const mode = urlParams.get('mode');

    let searchUrl = `http://localhost:5000/${mode}`;

    if (query) {
        search(searchUrl, query);
    }
});

document.getElementById('searchButton').addEventListener('click', function () {
    const mode = getSearchMode();
    const searchUrl = `http://localhost:5000/${mode}`;
    const query = document.getElementById('searchQuery').value;
    search(searchUrl, query);
});

function getSearchMode() {
    if (document.getElementById('mixSearch').checked) return 'mix_search';
    if (document.getElementById('phraseSearch').checked) return 'phrase_search';
    if (document.getElementById('proximitySearch').checked) return 'proximity_search';
    if (document.getElementById('rankedSearch').checked) return 'ranked_search';
    return 'search';
}

function search(url, query) {
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
                results.innerHTML = '';
                data.results.forEach(result => {
                    results.innerHTML += `<div class="result-item">
                    <h3><a href="${result.url}" target="_self">${result.title}</a></h3>
                    <p>${result.summary}</p>
                    <small>Tags: ${result.file_name.replace(/\//g, '  ').replace(/\.json$/, '')}</small>
                </div>`;
                });
            } else {
                results.innerHTML = '<p>No results found.</p>';
            }
            // results.innerHTML = ''; // 清空当前的结果
            // if (Array.isArray(data.results)) {
            //     data.results.forEach(result => {
            //         const div = document.createElement('div');
            //         div.className = 'result-item';
            //         div.innerHTML = `<h3><a href="${result.url}" target="_self">${result.title}</a></h3>
            //                          <p>${result.summary}</p>
            //                          <small>Tags: ${result.file_name}</small>`;
            //         results.appendChild(div);
            //     });
            // } else {
            //     results.innerHTML = '<p>No results found.</p>';
            // }            
        })
        .catch(error => {
            console.error('Error:', error);
            results.innerHTML = 'Unexpected Error';
        });
}
