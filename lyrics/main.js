document.addEventListener('DOMContentLoaded', () => {
    const songsTableBody = document.querySelector('#songs-table tbody');
    const searchBar = document.getElementById('search-bar');
    const searchButton = document.getElementById('search-button');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageNumbersContainer = document.getElementById('page-numbers');
    const itemsPerPageSelect = document.getElementById('items-per-page');

    let songs = [];
    let filteredSongs = [];
    let currentPage = 1;
    let itemsPerPage = parseInt(itemsPerPageSelect.value, 10);
    let sortColumn = 'englishname';
    let sortDirection = 'asc';

    async function fetchSongs() {
        try {
            const response = await fetch('/lyrics/songs.json');
            songs = await response.json();
            loadFromURL();
            performSearch(); // Perform initial search based on URL
            sortSongs(sortColumn, true); // Apply initial sort
        } catch (error) {
            console.error('Error fetching songs:', error);
        }
    }

    function renderTable() {
        songsTableBody.innerHTML = '';
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedSongs = filteredSongs.slice(start, end);

        paginatedSongs.forEach(song => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><a href="/lyrics/songs/${song.id}.html">${song.englishname}</a></td>
                <td><a href="/lyrics/songs/${song.id}.html">${song.mienthainame}</a></td>
                <td><a href="/lyrics/songs/${song.id}.html">${song.thainame}</a></td>
            `;
            songsTableBody.appendChild(row);
        });
    }

    function setupPagination() {
        pageNumbersContainer.innerHTML = '';
        const pageCount = Math.ceil(filteredSongs.length / itemsPerPage);

        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === pageCount;

        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(pageCount, currentPage + 2);

        if (currentPage <= 3) {
            endPage = Math.min(pageCount, 5);
        }

        if (currentPage > pageCount - 3) {
            startPage = Math.max(1, pageCount - 4);
        }

        for (let i = startPage; i <= endPage; i++) {
            const pageNumberBtn = document.createElement('button');
            pageNumberBtn.textContent = i;
            pageNumberBtn.classList.add('page-number');
            if (i === currentPage) {
                pageNumberBtn.classList.add('active');
            }
            pageNumberBtn.addEventListener('click', () => {
                currentPage = i;
                renderTable();
                setupPagination();
                updateURL();
            });
            pageNumbersContainer.appendChild(pageNumberBtn);
        }
    }

    function sortSongs(column, preserveDirection = false) {
        if (!preserveDirection) {
            if (sortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = column;
                sortDirection = 'asc';
            }
        }

        filteredSongs.sort((a, b) => {
            const nameA = a[sortColumn] || '';
            const nameB = b[sortColumn] || '';
            return sortDirection === 'asc' 
                ? nameA.localeCompare(nameB) 
                : nameB.localeCompare(nameA);
        });

        updateSortIndicators();
        renderTable();
        setupPagination();
        updateURL();
    }

    function updateSortIndicators() {
        document.querySelectorAll('#songs-table th').forEach(th => {
            th.classList.remove('sorted-asc', 'sorted-desc');
            if (th.dataset.column === sortColumn) {
                th.classList.add(sortDirection === 'asc' ? 'sorted-asc' : 'sorted-desc');
            }
        });
    }

    function updateURL() {
        const params = new URLSearchParams(window.location.search);
        params.set('page', currentPage);
        params.set('limit', itemsPerPage);
        params.set('sort', sortColumn);
        params.set('dir', sortDirection);
        const searchTerm = searchBar.value;
        if (searchTerm) {
            params.set('search', searchTerm);
        } else {
            params.delete('search');
        }
        window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
    }

    function performSearch() {
        const searchTerm = searchBar.value.toLowerCase();
        filteredSongs = songs.filter(song => 
            (song.englishname || '').toLowerCase().includes(searchTerm) ||
            (song.mienthainame || '').toLowerCase().includes(searchTerm) ||
            (song.thainame || '').toLowerCase().includes(searchTerm)
        );
        currentPage = 1;
        sortSongs(sortColumn, true); // Re-apply current sort
    }

    function loadFromURL() {
        const params = new URLSearchParams(window.location.search);
        currentPage = parseInt(params.get('page'), 10) || 1;
        itemsPerPage = parseInt(params.get('limit'), 10) || 100;
        itemsPerPageSelect.value = itemsPerPage;
        sortColumn = params.get('sort') || 'englishname';
        sortDirection = params.get('dir') || 'asc';
        searchBar.value = params.get('search') || '';
    }

    // Event Listeners
    searchButton.addEventListener('click', performSearch);
    searchBar.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });

    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
            setupPagination();
            updateURL();
        }
    });

    nextPageBtn.addEventListener('click', () => {
        const pageCount = Math.ceil(filteredSongs.length / itemsPerPage);
        if (currentPage < pageCount) {
            currentPage++;
            renderTable();
            setupPagination();
            updateURL();
        }
    });

    itemsPerPageSelect.addEventListener('change', () => {
        itemsPerPage = parseInt(itemsPerPageSelect.value, 10);
        currentPage = 1;
        renderTable();
        setupPagination();
        updateURL();
    });

    document.querySelectorAll('#songs-table th').forEach(th => {
        th.addEventListener('click', () => {
            sortSongs(th.dataset.column);
        });
    });

    // Initial Load
    fetchSongs();
});
