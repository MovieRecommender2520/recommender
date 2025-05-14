let genreMap = {};
const movieCache = {};


document.addEventListener('DOMContentLoaded', async () => {
    await loadGenreMaps();

    const input = document.getElementById('search-input');
    const autocompleteList = document.getElementById('autocomplete-list');
    const recommendationBox = document.getElementById('recommendation-area');

    setUpAutocomplete();

    // Fade-in animation after all setup
    document.body.classList.add('loaded');

    function setUpAutocomplete() {
        const input = document.getElementById('search-input');
        const autocompleteList = document.getElementById('autocomplete-list');
        let activeIndex = -1;
    
        input.addEventListener('input', () => {
            const query = input.value.toLowerCase().trim();
            autocompleteList.innerHTML = '';
            activeIndex = -1;
        
            if (query === '') {
                autocompleteList.classList.remove('active'); // hide it if input is empty
                return;
            }
        
            const matches = movieTitles
                .filter(title => title.toLowerCase().includes(query))
                .slice(0, 5);
        
            if (matches.length) {
                autocompleteList.classList.add('active');   // show dropdown
            } else {
                autocompleteList.classList.remove('active');
            }
        
            matches.forEach(title => {
                const li = document.createElement('li');
                li.textContent = title;
        
                li.onclick = () => {
                    input.value = title;
                    autocompleteList.innerHTML = '';
                    autocompleteList.classList.remove('active');  // hide after select
                    fetchRecommendations(title);
                };
        
                autocompleteList.appendChild(li);
            });
        });
        
    
        input.addEventListener('keydown', (e) => {
            const items = autocompleteList.querySelectorAll('li');
            if (!items.length) return;
    
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                activeIndex = (activeIndex + 1) % items.length;
                updateActive(items);
            }
    
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                activeIndex = (activeIndex - 1 + items.length) % items.length;
                updateActive(items);
            }
    
            if (e.key === 'Enter') {
                e.preventDefault();
                if (activeIndex > -1) {
                    items[activeIndex].click();
                }
            }
        });
    
        function updateActive(items) {
            items.forEach(item => item.classList.remove('active'));
            if (items[activeIndex]) {
                items[activeIndex].classList.add('active');
            }
        }
    }
    

    async function fetchRecommendations(title) {
        const recommendationBox = document.getElementById('recommendation-area');
        recommendationBox.removeAttribute('hidden');
    
        // Step 1: Show shimmer placeholders
        recommendationBox.innerHTML = `
            <h3>Loading Recommendations...</h3>
            <div class="recommendation-table">
                ${Array.from({ length: 5 }).map(() => `
                    <div class="movie-card loading"></div>
                `).join('')}
            </div>
        `;
    
        // Step 2: Fetch titles from Flask
        const res = await fetch(`/recommend?movie=${encodeURIComponent(title)}`);
        const titles = await res.json();
    
        // Step 3: Fetch TMDB data for each title
        const results = await Promise.all(titles.map(async (title) => {
            const movie = await fetchTMDBData(title);
            return {
                title: title,
                poster: movie?.poster_path ? `https://image.tmdb.org/t/p/w200${movie.poster_path}` : null,
                link: movie ? `https://www.themoviedb.org/movie/${movie.id}` : '#',
                year: movie?.release_date?.slice(0, 4),
                genres: Array.isArray(movie?.genre_ids)
                    ? movie.genre_ids.map(id => genreMap[id]).filter(Boolean).slice(0, 3)
                    : []
            };
        }));
    
        // Step 4: Replace shimmer with real movie cards
        recommendationBox.innerHTML = `
            <h3>Recommended Movies</h3>
            <div class="recommendation-table">
                ${results.map((movie, i) => `
                    <a href="${movie.link}" class="movie-card" style="animation-delay: ${i * 0.05}s" target="_blank">
                        ${movie.poster ? `<img src="${movie.poster}" alt="${movie.title} poster">` : ''}
                        <div class="movie-info">
                            <h4>${movie.title}</h4>
                            ${movie.year ? `<span class="year">${movie.year}</span>` : ''}
                            <div class="genre-badges">
                                ${movie.genres.map(g => `<span class="genre-badge">${g}</span>`).join('')}
                            </div>
                        </div>
                    </a>
                `).join('')}
            </div>
        `;
    }
    

    async function fetchTMDBData(title) {
        if (movieCache[title]) {
            console.log(`Loaded from cache: ${title}`);
            return movieCache[title];
        }
    
        const res = await fetch(`/tmdb/${encodeURIComponent(title)}`);
        const data = await res.json();
        const result = data.results?.[0];
    
        movieCache[title] = result; // store it
        return result;
    }
    

    async function loadGenreMaps() {
        const res = await fetch("/tmdb-genres");
        const data = await res.json();
        genreMap = Object.fromEntries(data.genres.map(g => [g.id, g.name]));
    }
});

document.addEventListener('click', (e) => {
    if (e.target.closest('.movie-card')) {
        const card = e.target.closest('.movie-card');
        card.style.animation = 'pop 0.2s ease';
        setTimeout(() => card.style.animation = '', 200);
    }
});
