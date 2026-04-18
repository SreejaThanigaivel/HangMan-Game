// The identical Python word array migrated to JS
const WORDS = [
    "python", "turtle", "programming", "hangman", "keyboard",
    "computer", "algorithm", "variable", "function", "library",
    "elephant", "dolphin", "volcano", "gravity", "mystery",
    "journey", "crystal", "lantern", "sunrise", "thunder",
    "blanket", "fashion", "diamond", "cabinet", "network"
];

// Configuration
const MAX_WRONG = 6;

// Track game states
let targetWord = "";
let guessedLetters = new Set();
let wrongCount = 0;
let gameOver = false;

// DOM Elements Initialization
const wordContainer = document.getElementById("word-container");
const keyboardContainer = document.getElementById("keyboard-container");
const wrongCountDisplay = document.getElementById("wrong-count");
const overlay = document.getElementById("overlay");
const modalTitle = document.getElementById("modal-title");
const targetWordDisplay = document.getElementById("target-word");
const restartBtn = document.getElementById("restart-btn");

/**
 * Initializes/Restarts a single session of Hangman.
 */
function initGame() {
    // Reset state trackers
    guessedLetters.clear();
    wrongCount = 0;
    gameOver = false;

    // Pick a random word from the WORDS array
    targetWord = WORDS[Math.floor(Math.random() * WORDS.length)].toUpperCase();

    // Reset UI Counters
    wrongCountDisplay.innerText = wrongCount;
    overlay.classList.add("hidden"); // Remove modal popup

    // Smoothly remove visibly rendered line components (SVG) from the screen
    for (let i = 0; i < MAX_WRONG; i++) {
        const part = document.getElementById(`part-${i}`);
        if (part) part.classList.remove("visible");
    }

    // Run necessary render updates
    renderWord();
    renderKeyboard();
}

/**
 * Iterates through the target word and displays the letter placeholder lines,
 * elevating letters if successfully guessed.
 */
function renderWord() {
    wordContainer.innerHTML = "";

    for (const char of targetWord) {
        const letterBox = document.createElement("div");
        letterBox.className = "letter-box";

        // Populate the inner box if the letter was in our Guessed Set
        if (guessedLetters.has(char)) {
            letterBox.innerText = char;
            letterBox.classList.add("revealed"); // Add styling for the reveal bounce jump
        }

        wordContainer.appendChild(letterBox);
    }
}

/**
 * Show missed letters after user runs out of guesses completely.
 */
function revealFullWordMissed() {
    const letterBoxes = wordContainer.children;
    for (let i = 0; i < targetWord.length; i++) {
        const char = targetWord[i];
        if (!guessedLetters.has(char)) {
            letterBoxes[i].innerText = char;
            letterBoxes[i].classList.add("missed"); // Colors the unrevealed ones differently.
        }
    }
}

/**
 * Quick loop iterating over letters to determine if every unique letter was successfully guessed.
 */
function checkWin() {
    for (const char of targetWord) {
        if (!guessedLetters.has(char)) {
            return false;
        }
    }
    return true;
}

/**
 * The primary interaction logic running every time a Letter button or Keystroke occurs.
 * @param {string} letter - E.g. "A"
 */
function handleGuess(letter) {
    // Escape clause if Game Over occurred or if Letter is already in cache
    if (gameOver || guessedLetters.has(letter)) return;

    guessedLetters.add(letter);

    // Lookup UI Key instance
    const button = document.getElementById(`key-${letter}`);
    if (button) button.disabled = true;

    if (targetWord.includes(letter)) {
        // --- Correct Guess ---
        if (button) button.classList.add("correct");
        renderWord(); // refresh display

        if (checkWin()) {
            endGame(true);
        }
    } else {
        // --- Incorrect Guess ---
        if (button) button.classList.add("wrong");

        // Re-veil the corresponding hidden line in the SVG
        const part = document.getElementById(`part-${wrongCount}`);
        if (part) part.classList.add("visible");

        wrongCount++;
        wrongCountDisplay.innerText = wrongCount;

        if (wrongCount >= MAX_WRONG) {
            endGame(false);
            revealFullWordMissed();
        }
    }
}

/**
 * Fires the pop-up modal and updates appropriate message texts.
 * @param {boolean} isWin 
 */
function endGame(isWin) {
    gameOver = true;
    targetWordDisplay.innerText = targetWord;

    if (isWin) {
        modalTitle.innerText = "🎉 YOU WON!";
        modalTitle.className = "win";
    } else {
        modalTitle.innerText = "💀 GAME OVER";
        modalTitle.className = "lose";
    }

    // Add small timeout equivalent to CSS transition speeds so lines can snap visually 
    // before dimming down.
    setTimeout(() => {
        overlay.classList.remove("hidden");
    }, 450);
}

/**
 * Generate standard QWERTY letter groups interactively bound with `handleGuess` logic events. 
 */
function renderKeyboard() {
    keyboardContainer.innerHTML = "";

    const rows = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ];

    rows.forEach(rowGroup => {
        // Group row elements together
        const rowDiv = document.createElement("div");
        rowDiv.className = "keyboard-row";

        for (const char of rowGroup) {
            const btn = document.createElement("button");
            btn.className = "key-btn";
            btn.id = `key-${char}`;
            btn.innerText = char;

            // Interaction Hook
            btn.addEventListener("click", () => handleGuess(char));

            rowDiv.appendChild(btn);
        }
        keyboardContainer.appendChild(rowDiv);
    });
}

/** 
 * Connect global keyboard typing features natively 
 */
window.addEventListener("keydown", (e) => {
    // Only capture plain alphabetic keys
    if (/^[a-zA-Z]$/.test(e.key)) {
        handleGuess(e.key.toUpperCase());
    }

    // Check if 'Space' command requested a restart
    if (e.code === "Space") {
        e.preventDefault(); // Removes generic space scrolling jump event

        // Enable immediate resets in all states
        initGame();
    }
});

// Finally, enable modal replay click binding & Start Game Runtime
restartBtn.addEventListener("click", initGame);

// Load up application
initGame();
