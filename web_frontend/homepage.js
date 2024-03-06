document.getElementById('searchButton').addEventListener('click', function () {
    const query = document.getElementById('searchQuery').value;
    let searchMode = 'search'; // 默认为search模式
    if (document.getElementById('mixSearch').checked) {
        searchMode = 'mix_search';
    } else if (document.getElementById('phraseSearch').checked) {
        searchMode = 'phrase_search';
    } else if (document.getElementById('proximitySearch').checked) {
        searchMode = 'proximity_search';
    } else if (document.getElementById('rankedSearch').checked) {
        searchMode = 'ranked_search';
    }
    const searchPageUrl = `result.html?query=${encodeURIComponent(query)}&mode=${searchMode}`;
    window.location.href = searchPageUrl;
});




