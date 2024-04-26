// Create a full-screen overlay on a webpage
const overlay = document.createElement('div'); // Create a new div element
Object.assign(overlay.style, {
    position: 'fixed', // Fixed position so it doesn't scroll with the page
    zIndex: 999999, // Make sure it's on top of everything else
    top: 0, // Position at the top
    left: 0, // Position at the left
    width: '100%', // Full width
    height: '100%', // Full height
    background: 'rgba(0, 0, 0, 0.7)', // Semi-transparent black background
    color: '#fff', // White text
    fontSize: '24px',
    fontWeight: 'bold',
    display: 'flex', // Flex layout
    justifyContent: 'center',
    alignItems: 'center',
});
const textContent = document.createElement('div'); 
Object.assign(textContent.style, {
    textAlign: 'center',
});
textContent.textContent = 'Tavily AI: Analyzing Page';
overlay.appendChild(textContent);
document.body.append(overlay); // Add the overlay to the page
document.body.style.overflow = 'hidden'; // Hide the scrollbars
let dotCount = 0;
setInterval(() => {
    textContent.textContent = 'Tavily AI: Analyzing Page' + '.'.repeat(dotCount);
    dotCount = (dotCount + 1) % 4;
}, 1000);