// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let currentUser = null;
let studentProgress = null;

// DOM Utility
function $(id) { return document.getElementById(id); }

// API Functions 
async function apiRequest(endpoint, method = 'GET', data = null) {
    // Always return null to force local mode
    console.log('API request skipped, using local mode');
    return null;
}

// User Management
async function loginUser(username, isGuest = false) {
    handleLocalLogin(username, isGuest);
}

function handleLocalLogin(username, isGuest) {
    currentUser = {
        user_id: isGuest ? `guest_${Date.now()}` : `student_${Date.now()}`,
        name: isGuest ? 'Guest' : username,
        type: isGuest ? 'guest' : 'student'
    };
    
    localStorage.setItem('its_user', JSON.stringify(currentUser));
    $('welcome').innerText = `Welcome, ${currentUser.name}!`;
    
    loadProgress();
    setActive('navDashboard');
    showSection('sectionDashboard');
    
    showNotification(`Welcome ${currentUser.name}!`, 'info');
}

// Initialize default progress STRUCTURE
function getDefaultProgress() {
    return {
        quiz: { score: 0, total: 3, completed: false },
        practice: { completed: [], correct: 0, total: 5 },
        lastActivity: null
    };
}

// Progress Management 
async function loadProgress() {
    console.log('Loading progress...');
    
    if (!currentUser) {
        const storedUser = JSON.parse(localStorage.getItem('its_user') || 'null');
        if (storedUser) {
            currentUser = storedUser;
            console.log('Loaded user from storage:', currentUser.name);
        } else {
            console.log('No user logged in');
            return;
        }
    }
    
    //  use localStorage 
    try {
        const allProgress = JSON.parse(localStorage.getItem('its_progress') || '{}');
        console.log('All progress in storage:', allProgress);
        
        if (allProgress[currentUser.name]) {
            studentProgress = allProgress[currentUser.name];
            console.log('Loaded progress for user:', currentUser.name, studentProgress);
        } else {
            // Initialize fresh progress for new user
            studentProgress = getDefaultProgress();
            console.log('Created NEW progress for user:', currentUser.name);
            
            // Save initial progress
            allProgress[currentUser.name] = studentProgress;
            localStorage.setItem('its_progress', JSON.stringify(allProgress));
            console.log('Saved initial progress to localStorage');
        }
    } catch (error) {
        console.error('Error loading progress:', error);
        // Initialize fresh progress
        studentProgress = getDefaultProgress();
    }
    
    updateProgressDisplay();
}

async function saveProgress() {
    if (!currentUser || !studentProgress) {
        console.error('Cannot save: No user or progress');
        return;
    }
    
    console.log('SAVING progress for:', currentUser.name, studentProgress);
    
    try {
        // save to localStorage
        const allProgress = JSON.parse(localStorage.getItem('its_progress') || '{}');
        allProgress[currentUser.name] = studentProgress;
        localStorage.setItem('its_progress', JSON.stringify(allProgress));
        
        console.log('Progress saved to localStorage');
        console.log('Current localStorage:', localStorage.getItem('its_progress'));
        
        updateProgressDisplay();
    } catch (error) {
        console.error('Error saving progress:', error);
    }
}

// Update progress displays 
function updateProgressDisplay() {
    if (!studentProgress) {
        console.log('No progress data to display');
        return;
    }
    
    console.log('Updating display with:', studentProgress);
    
    // Calculate percentages
    const quizScore = studentProgress.quiz.score || 0;
    const quizTotal = studentProgress.quiz.total || 3;
    const quizPercent = studentProgress.quiz.completed ? 
        Math.round((quizScore / quizTotal) * 100) : 0;
    
    const practiceCorrect = studentProgress.practice.correct || 0;
    const practiceTotal = studentProgress.practice.total || 5;
    const practicePercent = practiceTotal > 0 ? 
        Math.round((practiceCorrect / practiceTotal) * 100) : 0;
    
    const overallPercent = Math.round((quizPercent + practicePercent) / 2);
    
    console.log('Calculated percentages - Quiz:', quizPercent, 'Practice:', practicePercent, 'Overall:', overallPercent);
    
    // Update progress section
    if ($('quizScore')) {
        $('quizScore').textContent = quizPercent + '%';
        console.log('Set quizScore to:', quizPercent + '%');
    }
    
    if ($('practiceScore')) {
        $('practiceScore').textContent = practicePercent + '%';
        console.log('Set practiceScore to:', practicePercent + '%');
    }
    
    if ($('completedExercises')) {
        const completedCount = studentProgress.practice.completed ? studentProgress.practice.completed.length : 0;
        $('completedExercises').textContent = completedCount + '/' + practiceTotal;
        console.log('Set completedExercises to:', completedCount + '/' + practiceTotal);
    }
    
    if ($('progFill')) {
        $('progFill').style.width = overallPercent + '%';
        console.log('Set progFill width to:', overallPercent + '%');
    }
    
    if ($('progText')) {
        $('progText').textContent = overallPercent + '% Complete';
        console.log('Set progText to:', overallPercent + '% Complete');
    }
    
    // Update dashboard
    if ($('dashProgress')) {
        $('dashProgress').style.width = overallPercent + '%';
        console.log('Set dashProgress width to:', overallPercent + '%');
    }
    
    if ($('dashText')) {
        $('dashText').textContent = overallPercent + '% Complete';
        console.log('Set dashText to:', overallPercent + '% Complete');
    }
    
    if ($('dashQuizScore')) {
        $('dashQuizScore').textContent = quizPercent + '%';
        console.log('Set dashQuizScore to:', quizPercent + '%');
    }
    
    if ($('dashPracticeScore')) {
        $('dashPracticeScore').textContent = practicePercent + '%';
        console.log('Set dashPracticeScore to:', practicePercent + '%');
    }
    
    // Update recent activity
    updateRecentActivity();
}

// Update recent activity log
function updateRecentActivity() {
    const activityDiv = $('recentActivity');
    const dashActivityDiv = $('dashActivity');
    
    if (!activityDiv && !dashActivityDiv) return;
    
    if (!studentProgress) {
        const noActivityMsg = '<p>No activity yet. Complete quizzes and practice exercises to see your progress!</p>';
        if (activityDiv) activityDiv.innerHTML = noActivityMsg;
        if (dashActivityDiv) dashActivityDiv.innerHTML = '<p>No recent activity. Start learning to see your progress!</p>';
        return;
    }
    
    let html = '';
    let dashHtml = '';
    
    if (studentProgress.quiz.completed) {
        const score = studentProgress.quiz.score || 0;
        const total = studentProgress.quiz.total || 3;
        html += `<p>✓ Completed quiz with score: ${score}/${total}</p>`;
        dashHtml += `<li>✓ Quiz completed: ${score}/${total} correct</li>`;
    }
    
    if (studentProgress.practice && studentProgress.practice.completed && studentProgress.practice.completed.length > 0) {
        const completedCount = studentProgress.practice.completed.length;
        const correctCount = studentProgress.practice.correct || 0;
        const totalCount = studentProgress.practice.total || 5;
        
        html += `<p>✓ Completed ${completedCount} practice exercises</p>`;
        html += `<p>✓ Practice score: ${correctCount}/${totalCount} correct</p>`;
        
        dashHtml += `<li>✓ Practice: ${correctCount}/${totalCount} correct</li>`;
        dashHtml += `<li>✓ Exercises completed: ${completedCount}</li>`;
    }
    
    if (studentProgress.lastActivity) {
        html += `<p><small>Last activity: ${studentProgress.lastActivity}</small></p>`;
        dashHtml += `<li><small>Last updated: ${studentProgress.lastActivity}</small></li>`;
    }
    
    if (activityDiv) {
        activityDiv.innerHTML = html || '<p>No recent activity.</p>';
    }
    
    if (dashActivityDiv) {
        dashActivityDiv.innerHTML = dashHtml ? `<ul style="list-style: none; padding: 0;">${dashHtml}</ul>` : '<p>No recent activity.</p>';
    }
}

// Navigation
const topNav = ['navHome', 'navQuiz', 'navShapes', 'navProgress', 'navPractice', 'navDashboard'];

function setActive(id) {
    topNav.forEach(n => $(n).classList.remove('active'));
    $(id).classList.add('active');
}

function showSection(id) {
    ['sectionHome', 'sectionQuiz', 'sectionShapes', 'sectionProgress', 'sectionPractice', 'sectionDashboard']
        .forEach(s => $(s).classList.add('hidden'));
    $(id).classList.remove('hidden');
}

// Initialize navigation
function initNavigation() {
    $('navHome').addEventListener('click', () => {
        setActive('navHome');
        showSection('sectionHome');
    });
    
    $('navQuiz').addEventListener('click', () => {
        setActive('navQuiz');
        showSection('sectionQuiz');
    });
    
    $('navShapes').addEventListener('click', () => {
        setActive('navShapes');
        showSection('sectionShapes');
    });
    
    $('navProgress').addEventListener('click', () => {
        setActive('navProgress');
        showSection('sectionProgress');
        loadProgress(); // Load progress student visit progress page
    });
    
    $('navPractice').addEventListener('click', () => {
        setActive('navPractice');
        showSection('sectionPractice');
        loadPracticeExercises();
    });
    
    $('navDashboard').addEventListener('click', () => {
        setActive('navDashboard');
        showSection('sectionDashboard');
        loadProgress(); // Load progress when student visit dashboard
    });
}

// Login handlers
function initLogin() {
    $('btnLogin').addEventListener('click', () => {
        const name = $('studentName').value.trim();
        if (!name) {
            showNotification('Please enter your name', 'error');
            return;
        }
        loginUser(name, false);
    });
    
    $('btnGuest').addEventListener('click', () => {
        loginUser('', true);
    });
}

// Dashboard navigation
function initDashboard() {
    $('goQuiz').addEventListener('click', () => {
        setActive('navQuiz');
        showSection('sectionQuiz');
    });
    
    $('goShapes').addEventListener('click', () => {
        setActive('navShapes');
        showSection('sectionShapes');
    });
    
    $('goPractice').addEventListener('click', () => {
        setActive('navPractice');
        showSection('sectionPractice');
        loadPracticeExercises();
    });
}

// Quiz functionality 
let quizData = [
    { q: 'How many faces does a cube have?', opts: ['4', '6', '8'], a: '6' },
    { q: 'Volume of a cylinder?', opts: ['πr²h', '2πrh', 'πrh'], a: 'πr²h' },
    { q: 'Surface area of a sphere?', opts: ['4πr²', 'πr²', '2πr'], a: '4πr²' }
];
let qIndex = 0;
let qScore = 0;

function loadQuiz() {
    if (quizData.length === 0) {
        $('quizQuestion').innerText = 'No quiz questions available.';
        $('quizOptions').innerHTML = '';
        return;
    }
    
    const Q = quizData[qIndex];
    $('quizQuestion').innerText = Q.q;
    const opts = $('quizOptions');
    opts.innerHTML = '';
    
    Q.opts.forEach(o => {
        const d = document.createElement('div');
        d.className = 'quiz-option';
        d.innerText = o;
        d.onclick = () => {
            if (o === Q.a) {
                d.style.background = '#d4ffd9';
                qScore++;
            } else {
                d.style.background = '#ffd7d7';
            }
            Array.from(opts.children).forEach(c => c.style.pointerEvents = 'none');
        };
        opts.appendChild(d);
    });
}

async function submitQuizResults() {
    console.log('Quiz completed! Score:', qScore, 'out of', quizData.length);
    
    // Ensure progress exists
    if (!studentProgress) {
        studentProgress = getDefaultProgress();
    }
    
    // Update progress
    studentProgress.quiz.score = qScore;
    studentProgress.quiz.total = quizData.length;
    studentProgress.quiz.completed = true;
    studentProgress.lastActivity = new Date().toLocaleString();
    
    console.log('Updated studentProgress:', studentProgress);
    
    // Save progress
    await saveProgress();
    
    // Show notification
    showNotification(`Quiz finished! Score: ${qScore}/${quizData.length}`, 'success');
    
    // Reset for next quiz
    qIndex = 0;
    qScore = 0;
    loadQuiz();
}

// AI tutor Chat Functionality
async function sendMessage() {
    const input = $('chatInput');
    const question = input.value.trim();
    
    if (!question) return;
    
    addMessage(question, true);
    input.value = '';
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message ai-message';
    typingIndicator.id = 'typingIndicator';
    typingIndicator.innerHTML = '<em>AI Tutor is thinking...</em>';
    $('chatMessages').appendChild(typingIndicator);
    $('chatMessages').scrollTop = $('chatMessages').scrollHeight;
    
    // Simulate AI tutor  thinking
    setTimeout(() => {
        // Remove typing indicator
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
        
        // Simple AI tutor response
        const response = getLocalAIResponse(question);
        addMessage(response);
    }, 1000);
}

function getLocalAIResponse(question) {
    const lowerQuestion = question.toLowerCase();
    
    if (lowerQuestion.includes('hello') || lowerQuestion.includes('hi')) {
        return 'Hello! I\'m your geometry tutor. Ask me about shapes and formulas!';
    }
    
    return 'I can help with geometry formulas. Please try asking about specific shapes like cubes, spheres, or cylinders.';
}

function addMessage(text, isUser = false) {
    const messages = $('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
    messageDiv.textContent = text;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

function handleChatInput(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function askSuggestedQuestion(question) {
    $('chatInput').value = question;
    sendMessage();
}

// Practice functionality 
let practiceExercises = [
    {
        question: "Calculate the volume of a cube with side length 4 units.",
        answer: 64,
        hint: "Volume of cube = side³"
    },
    {
        question: "Find the surface area of a sphere with radius 5 units. (Use π = 3.14)",
        answer: 314,
        hint: "Surface area of sphere = 4πr²"
    },
    {
        question: "Calculate the area of a triangle with base 10 units and height 6 units.",
        answer: 30,
        hint: "Area of triangle = ½ × base × height"
    },
    {
        question: "Find the volume of a cylinder with radius 3 units and height 8 units. (Use π = 3.14)",
        answer: 226.08,
        hint: "Volume of cylinder = πr²h"
    },
    {
        question: "Calculate the perimeter of a rectangle with length 12 units and width 7 units.",
        answer: 38,
        hint: "Perimeter of rectangle = 2(length + width)"
    }
];
let practiceAnswers = {};

function loadPracticeExercises() {
    // Clear the practice content
    $('practiceContent').innerHTML = '';
    
    // Create exercise elements dynamically
    practiceExercises.forEach((exercise, index) => {
        const exerciseNum = index + 1;
        practiceAnswers[exerciseNum] = exercise.answer;
        
        const exerciseHTML = `
            <div class="practice-activity">
                <h3>Activity ${exerciseNum}</h3>
                <p>${exercise.question}</p>
                <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">
                    <em>Hint: ${exercise.hint}</em>
                </div>
                <div class="input-group">
                    <input type="number" id="practice${exerciseNum}" placeholder="Your answer" step="any">
                    <button onclick="checkPractice(${exerciseNum})">Check Answer</button>
                </div>
                <div id="feedback${exerciseNum}" class="feedback"></div>
            </div>
        `;
        $('practiceContent').innerHTML += exerciseHTML;
    });
    
    // Initialize practice total in progress
    if (studentProgress) {
        studentProgress.practice.total = practiceExercises.length;
    }
}

async function checkPractice(activityNum) {
    // Ensure progress exists
    if (!studentProgress) {
        studentProgress = getDefaultProgress();
    }
    
    const input = $('practice' + activityNum);
    const feedback = $('feedback' + activityNum);
    const userAnswer = parseFloat(input.value);
    const correctAnswer = practiceAnswers[activityNum];
    
    if (isNaN(userAnswer)) {
        feedback.textContent = 'Please enter a valid number';
        feedback.className = 'feedback incorrect';
        return;
    }
    
    // Allow margin of error for decimal answers
    const margin = activityNum === 2 || activityNum === 4 ? 0.1 : 1;
    const isCorrect = Math.abs(userAnswer - correctAnswer) <= margin;
    
    if (isCorrect) {
        feedback.textContent = '✓ Correct! Well done!';
        feedback.className = 'feedback correct';
        input.style.background = '#d4ffd9';
        
        // Update progress
        if (!studentProgress.practice.completed.includes(activityNum)) {
            studentProgress.practice.completed.push(activityNum);
            studentProgress.practice.correct++;
            studentProgress.lastActivity = new Date().toLocaleString();
            
            console.log('Practice correct! Updated progress:', studentProgress);
            
            await saveProgress();
        }
    } else {
        feedback.textContent = '✗ Incorrect. Try again!';
        feedback.className = 'feedback incorrect';
        input.style.background = '#ffd7d7';
        
        if (!studentProgress.practice.completed.includes(activityNum)) {
            studentProgress.practice.completed.push(activityNum);
            studentProgress.lastActivity = new Date().toLocaleString();
            console.log('Practice incorrect. Updated progress:', studentProgress);
            await saveProgress();
        }
    }
}

async function resetPractice() {
    // Ensure progress exists
    if (!studentProgress) {
        studentProgress = getDefaultProgress();
    }
    
    // Clear all practice inputs
    for (let i = 1; i <= studentProgress.practice.total; i++) {
        const input = $('practice' + i);
        const feedback = $('feedback' + i);
        if (input) {
            input.value = '';
            input.style.background = '';
        }
        if (feedback) {
            feedback.textContent = '';
            feedback.className = 'feedback';
        }
    }
    
    // Reset practice progress
    studentProgress.practice.completed = [];
    studentProgress.practice.correct = 0;
    studentProgress.lastActivity = new Date().toLocaleString();
    await saveProgress();
    
    showNotification('Practice activities reset', 'info');
}

// Utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background: ${type === 'error' ? '#ff6b6b' : type === 'success' ? '#51cf66' : '#339af0'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('App initialized');
    
    // Initialize all modules
    initNavigation();
    initLogin();
    initDashboard();
    
    // Initialize quiz
    loadQuiz();
    $('quizNext').addEventListener('click', async () => {
        qIndex++;
        if (qIndex >= quizData.length) {
            await submitQuizResults();
        } else {
            loadQuiz();
        }
    });
    
    // Check if user is already logged in
    const storedUser = JSON.parse(localStorage.getItem('its_user') || 'null');
    if (storedUser) {
        currentUser = storedUser;
        $('welcome').innerText = `Welcome back, ${currentUser.name || 'Guest'}!`;
        loadProgress();
    }
    
    console.log('Initialization complete');
});