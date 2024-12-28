/* File JavaScript (script.js) */
const fireworksContainer = document.getElementById('fireworks');

function createFirework() {
    const firework = document.createElement('div');
    firework.classList.add('firework');
    firework.style.left = Math.random() * 100 + '%';
    firework.style.bottom = Math.random() * 100 + 'vh';
    firework.style.animationDuration = Math.random() * 2 + 1 + 's';
    fireworksContainer.appendChild(firework);

    setTimeout(() => {
        firework.remove();
    }, 4000);
}

setInterval(createFirework, 350);

// RSVP Button Animation
const rsvpButton = document.getElementById('rsvp-button');
rsvpButton.addEventListener('click', () => {
    alert('Grazie per aver confermato la tua partecipazione! Non vediamo l\'ora di festeggiare con te!');
});

// Countdown Timer
const countdownTimer = document.getElementById('countdown-timer');

function updateCountdown() {
    const now = new Date();
    const eventDate = new Date('2025-01-01T00:00:00');
    const timeDifference = eventDate - now;

    if (timeDifference <= 0) {
        countdownTimer.textContent = "Buon Anno!";
        return;
    }

    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

    countdownTimer.textContent = `${days}g ${hours}h ${minutes}m ${seconds}s`;
}

setInterval(updateCountdown, 1000);
updateCountdown();