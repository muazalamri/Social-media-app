let tasks = [];

function addTask() {
    const input = document.getElementById('taskInput');
    const priority = document.getElementById('prioritySelect').value;

    if (input.value.trim() === '') return;

    const task = {
        id: Date.now(),
        text: input.value.trim(),
        priority: priority,
        completed: false
    };

    tasks.push(task);
    input.value = '';
    renderTasks();
}

function deleteTask(id) {
    tasks = tasks.filter(task => task.id !== id);
    renderTasks();
}

function editTask(id) {
    const task = tasks.find(task => task.id === id);
    const newText = prompt('عدل المهمة:', task.text);

    if (newText !== null && newText.trim() !== '') {
        task.text = newText.trim();
        renderTasks();
    }
}

function togglePriority(id) {
    const task = tasks.find(task => task.id === id);
    const priorities = ['high',
        'normal',
        'low'];
    const currentIndex = priorities.indexOf(task.priority);
    task.priority = priorities[(currentIndex + 1) % priorities.length];
    renderTasks();
}

function renderTasks() {
    const taskList = document.getElementById('taskList');
    const filter = document.getElementById('filterSelect').value;

    taskList.innerHTML = '';

    // تصفية المهام حسب النوع المحدد
    const filteredTasks = filter === 'all'
    ? tasks: tasks.filter(task => task.priority === filter);

    // تحديث عداد المهام
    document.getElementById('taskCount').textContent =
    `${filteredTasks.length} مهام (${tasks.length} إجمالي)`;

    filteredTasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `task-item ${task.priority}`;

        const priorityText = {
            'high': 'مهم',
            'normal': 'عادي',
            'low': 'غير مهم'
        };

        li.innerHTML = `
        <div class="task-content">
        ${task.text} <small>(${priorityText[task.priority]})</small>
        </div>
        <div class="task-actions">
        <button onclick="togglePriority(${task.id})">change type</button>
        <button onclick="editTask(${task.id})">edit</button>
        <button onclick="deleteTask(${task.id})">del</button>
        <button onclick="shareTask(${task.id})" class="url-icon">🌐</button>
        </div>
        `;

        taskList.appendChild(li);
    });
}

function shareTask(id) {
    const task = tasks.find(task => task.id === id);
    const url = `${window.location.origin}${window.location.pathname}?task=${encodeURIComponent(task.text)}`;
    prompt('رابط المشاركة:', url);
}

// Load any task from URL if exists
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const taskFromUrl = urlParams.get('task');

    if (taskFromUrl) {
        document.getElementById('taskInput').value = taskFromUrl;
    }

    renderTasks();
};