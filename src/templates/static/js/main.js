// Utility functions
const showElement = (element) => {
    element.style.display = 'block';
    setTimeout(() => element.classList.add('show'), 10);
};

const hideElement = (element) => {
    element.classList.remove('show');
    setTimeout(() => element.style.display = 'none', 300);
};

const formatResults = (data) => {
    const resultContainer = document.getElementById('analysisResults');
    resultContainer.innerHTML = '';

    // Create a more structured and visually appealing display
    const resultCard = document.createElement('div');
    resultCard.className = 'result-card';

    for (const [key, value] of Object.entries(data)) {
        const section = document.createElement('div');
        section.className = 'result-section-item mb-4';
        
        const title = document.createElement('h6');
        title.className = 'text-primary mb-2';
        title.textContent = key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ');
        
        const content = document.createElement('div');
        content.className = 'result-content p-3 bg-light rounded';
        
        if (typeof value === 'object') {
            content.innerHTML = `<pre class="mb-0">${JSON.stringify(value, null, 2)}</pre>`;
        } else {
            content.textContent = value;
        }
        
        section.appendChild(title);
        section.appendChild(content);
        resultCard.appendChild(section);
    }

    resultContainer.appendChild(resultCard);
};

// Main form handling
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analysisForm');
    const loadingElement = document.querySelector('.loading');
    const errorElement = document.querySelector('.error-message');
    const resultElement = document.querySelector('.result-section');
    const urlInput = document.getElementById('url');

    // Add input validation
    urlInput.addEventListener('input', (e) => {
        const url = e.target.value;
        const isValid = url.match(/^https?:\/\/.+/);
        e.target.classList.toggle('is-invalid', !isValid && url.length > 0);
        e.target.classList.toggle('is-valid', isValid);
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        hideElement(errorElement);
        hideElement(resultElement);
        showElement(loadingElement);
        
        const url = urlInput.value;
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `url=${encodeURIComponent(url)}`
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                formatResults(data.data);
                showElement(resultElement);
            } else {
                errorElement.textContent = data.message;
                showElement(errorElement);
            }
        } catch (error) {
            errorElement.textContent = 'Une erreur est survenue lors de l\'analyse.';
            showElement(errorElement);
        } finally {
            hideElement(loadingElement);
        }
    });
}); 