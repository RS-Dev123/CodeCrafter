async function analyzeNews() {
    const inputField = document.getElementById('newsInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');
    const btnLoader = document.getElementById('btnLoader');
    const resultsContainer = document.getElementById('resultsContainer');
    const text = inputField.value.trim();

    if (!text) {
        alert("Please enter a claim to analyze.");
        return;
    }

    analyzeBtn.disabled = true;
    btnText.innerText = "Processing...";
    btnIcon.style.display = "none";
    btnLoader.style.display = "block";
    
    resultsContainer.style.display = 'none';
    document.getElementById('progressBar').style.width = '0%';

    try {
        const response = await fetch('http://127.0.0.1:5000/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ claim: text })
        });

        const data = await response.json();

        if (response.ok) {
            updateUI(text, data);
        } else {
            alert("Error: " + data.error);
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Server connection failed. Is app.py running?");
    } finally {
        analyzeBtn.disabled = false;
        btnText.innerText = "Analyze Deeply";
        btnIcon.style.display = "inline-block";
        btnLoader.style.display = "none";
    }
}

function updateUI(originalText, resultData) {
    const resultsContainer = document.getElementById('resultsContainer');
    const articlePreview = document.getElementById('articlePreview');
    const verdictCard = document.getElementById('verdictCard');
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictText = document.getElementById('verdictText');
    const categoryTag = document.getElementById('categoryTag');
    const confValue = document.getElementById('confValue');
    const progressBar = document.getElementById('progressBar');
    const reasonText = document.getElementById('reasonText');

    resultsContainer.style.display = 'flex';
    
    articlePreview.innerText = originalText.length > 250 ? originalText.substring(0, 250) + "..." : originalText;

    verdictCard.className = 'card verdict-card glass-panel slide-up';
    verdictIcon.className = 'icon-box pulse-slow';
    progressBar.className = 'progress-fill glow-shadow';

    verdictText.innerText = resultData.verdict;
    categoryTag.innerHTML = `<i class="fa-solid fa-tag" style="margin-right: 5px;"></i> ${resultData.category || "News"}`;
    
   
    animateValue(confValue, 0, resultData.confidence, 1500);
    
    typeWriter(reasonText, resultData.reason, 20);

    const verdictLower = resultData.verdict.toLowerCase();
    
    if (verdictLower.includes("fake") || verdictLower.includes("false")) {
        verdictCard.classList.add('verdict-fake');
        verdictIcon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
        progressBar.classList.add('fill-fake');
    } else if (verdictLower.includes("true")) {
        verdictCard.classList.add('verdict-true');
        verdictIcon.innerHTML = '<i class="fa-solid fa-shield-check"></i>';
        progressBar.classList.add('fill-true');
    } else {
        verdictIcon.innerHTML = '<i class="fa-solid fa-scale-balanced"></i>';
        progressBar.style.background = "linear-gradient(90deg, #4facfe, #00f2fe)";
        progressBar.style.boxShadow = "0 0 15px #00f2fe";
    }

    setTimeout(() => {
        progressBar.style.width = resultData.confidence + "%";
    }, 300);
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start) + "%";
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function typeWriter(element, text, speed) {
    element.innerHTML = '';
    let i = 0;
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}