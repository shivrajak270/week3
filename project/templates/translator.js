// translator.js

// Replace 'YOUR_GOOGLE_API_KEY' with your actual API key
const apiKey = 'YOUR_GOOGLE_API_KEY';

function translateText() {
    const sourceText = document.getElementById('source_text').value;
    const targetLanguage = document.getElementById('target_language').value;

    const url = `https://translation.googleapis.com/language/translate/v2?key=${apiKey}`;
    const data = {
        q: sourceText,
        target: targetLanguage
    };

    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const translatedText = data.data.translations[0].translatedText;
        document.getElementById('translated_text').innerText = translatedText;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
