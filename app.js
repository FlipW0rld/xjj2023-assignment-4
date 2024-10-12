// app.js

async function performSearch() {
    const query = document.getElementById('query').value;
    if (!query) {
        alert('Please enter a search query.');
        return;
    }

    const response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
    });

    const results = await response.json();
    displayResults(results);
    renderChart(results);
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';  

    results.forEach((result, index) => {
        const resultItem = document.createElement('div');
        resultItem.classList.add('result-item');

        resultItem.innerHTML = `
            <h2>Document ${index + 1}</h2>
            <p>${result.document}</p>
            <p class="similarity">Similarity: ${result.similarity}</p>
        `;

        resultsDiv.appendChild(resultItem);
    });
}


function renderChart(results) {
    const ctx = document.getElementById('chart').getContext('2d');
    const labels = results.map((_, i) => `Doc ${i + 1}`);
    const data = results.map(result => result.similarity);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cosine Similarity',
                data: data,
            }]
        },
    });
}
