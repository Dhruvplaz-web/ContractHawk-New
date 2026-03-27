document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const loadingTerminal = document.getElementById('loadingTerminal');

    if (!dropzone) return; // Only run on the dashboard page

    // 1. Click anywhere on the box to open file explorer
    dropzone.addEventListener('click', () => fileInput.click());

    // 2. Visual glow when dragging a file over the box
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('border-neonCyan', 'bg-neonCyan/5');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('border-neonCyan', 'bg-neonCyan/5');
    });

    // 3. Catch the file when dropped
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('border-neonCyan', 'bg-neonCyan/5');
        
        if (e.dataTransfer.files.length) {
            processFile(e.dataTransfer.files[0]);
        }
    });

    // 4. Catch the file if they clicked and browsed
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            processFile(this.files[0]);
        }
    });

    // 5. The Main Engine: Validate, Animate, and Send
    function processFile(file) {
        // Validate File Type
        const validExtensions = ['.pdf', '.docx'];
        const isValid = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
        
        if (!isValid) {
            alert('Security Error: Only PDF or DOCX files are permitted.');
            return;
        }

        // Validate Size (Max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('Upload Error: File exceeds the 10MB maximum limit.');
            return;
        }

        // --- INITIATE UI LOCKDOWN & ANIMATION ---
        dropzone.parentElement.classList.add('hidden'); // Hide dropzone
        loadingTerminal.classList.remove('hidden');     // Show terminal

        // Simulate terminal typing for better UX
        const logs = loadingTerminal.querySelectorAll('p');
        setTimeout(() => logs[0].classList.add('text-neonCyan'), 600);
        setTimeout(() => logs[1].classList.add('text-neonCyan'), 1800);

        // --- SEND TO PYTHON BACKEND ---
        const formData = new FormData();
        formData.append('document', file);

        // We are going to build this /api/scan route next!
        fetch('/api/scan', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Success! Make the final terminal text green and redirect
                logs[2].textContent = "> Audit complete. Redirecting to results...";
                logs[2].classList.replace('text-gray-500', 'text-green-500');
                
                setTimeout(() => {
                    // Redirect to the vault or comparison page with the new doc ID
                    window.location.href = `/vault`; 
                }, 1500);
            } else {
                alert('Engine Failure: ' + data.error);
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('A critical error occurred connecting to the ContractHawk engine.');
            location.reload();
        });
    }
});
