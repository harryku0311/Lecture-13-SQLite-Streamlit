// Global variables
let map;
let weatherData;
let selectedLocation = null;
let currentChart = null;
let markers = {};

// Initialize map when page loads
document.addEventListener('DOMContentLoaded', function () {
    initializeMap();
    loadWeatherData();
});

// Initialize Leaflet map
function initializeMap() {
    // Create map centered on Taiwan
    map = L.map('map').setView([23.5, 121.0], 8);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

// Load weather data from JSON
async function loadWeatherData() {
    try {
        const response = await fetch('weather_data.json');

        if (!response.ok) {
            throw new Error('Failed to load weather data');
        }

        weatherData = await response.json();

        // Update generated time
        document.getElementById('generatedTime').textContent =
            new Date(weatherData.generated_at).toLocaleString('zh-TW');

        // Create markers for each location
        createMarkers();

        // Hide loading, show content
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('content').classList.remove('hidden');

        // CRITICAL FIX: Force map to recalculate size after content is visible
        // This fixes the issue where clicks don't work until F12 is pressed
        setTimeout(() => {
            map.invalidateSize();
        }, 100);

    } catch (error) {
        console.error('Error loading weather data:', error);
        showError(error.message);
    }
}

// Create map markers for all locations - SIMPLIFIED VERSION
function createMarkers() {
    weatherData.locations.forEach(location => {
        // Determine marker color based on average temperature
        const color = getTemperatureColor(location.avg_temp);

        // Use simple circle marker instead of complex divIcon
        const marker = L.circleMarker([location.lat, location.lon], {
            radius: 15,
            fillColor: color,
            color: '#fff',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.9
        }).addTo(map);

        // Add popup with temperature label
        marker.bindPopup(`
            <div class="text-center p-2">
                <div class="font-bold text-lg text-gray-800">${location.name}</div>
                <div class="text-gray-600">${location.city}</div>
                <div class="text-blue-600 font-semibold mt-2 text-xl">${location.avg_temp}°C</div>
                <div class="text-sm text-gray-500 mt-1">${location.forecast_count} day forecast</div>
            </div>
        `);

        // IMPORTANT: Add click event that DEFINITELY works
        marker.on('click', function () {
            selectLocation(location);
        });

        // Also add permanent tooltip showing temperature
        marker.bindTooltip(`${location.avg_temp}°C`, {
            permanent: true,
            direction: 'center',
            className: 'temperature-label',
            offset: [0, 0]
        });

        // Store marker reference
        markers[location.name] = marker;
    });
}

// Get color based on temperature
function getTemperatureColor(temp) {
    if (temp >= 30) return '#dc2626'; // red-600
    if (temp >= 25) return '#ea580c'; // orange-600
    if (temp >= 20) return '#f59e0b'; // amber-600
    if (temp >= 15) return '#3b82f6'; // blue-600
    return '#0ea5e9'; // sky-600
}

// Select a location and display its data
function selectLocation(location) {
    console.log('Location clicked:', location.name); // Debug log

    selectedLocation = location;

    // Show location info section
    document.getElementById('locationInfo').classList.remove('hidden');

    // Update location name and city
    document.getElementById('selectedLocationName').textContent = location.name;
    document.getElementById('selectedLocationCity').textContent = `${location.city} Region`;

    // Calculate statistics
    const maxTemps = location.forecasts
        .map(f => f.max_temp)
        .filter(t => t !== null);
    const minTemps = location.forecasts
        .map(f => f.min_temp)
        .filter(t => t !== null);

    const highestMax = maxTemps.length > 0 ? Math.max(...maxTemps) : 0;
    const lowestMin = minTemps.length > 0 ? Math.min(...minTemps) : 0;

    // Update stats
    document.getElementById('avgTemp').textContent = `${location.avg_temp}°C`;
    document.getElementById('maxTemp').textContent = `${highestMax}°C`;
    document.getElementById('minTemp').textContent = `${lowestMin}°C`;

    // Create temperature chart
    createTemperatureChart(location);

    // Scroll to location info
    document.getElementById('locationInfo').scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    });
}

// Create temperature time-series chart
function createTemperatureChart(location) {
    const ctx = document.getElementById('temperatureChart').getContext('2d');

    // Destroy existing chart if any
    if (currentChart) {
        currentChart.destroy();
    }

    // Prepare data
    const dates = location.forecasts.map(f => f.date);
    const maxTemps = location.forecasts.map(f => f.max_temp);
    const minTemps = location.forecasts.map(f => f.min_temp);

    // Create new chart
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Maximum Temperature',
                    data: maxTemps,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: '#ef4444',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Minimum Temperature',
                    data: minTemps,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.parsed.y}°C`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Temperature (°C)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        callback: function (value) {
                            return value + '°C';
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Show error message
function showError(message) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
}
