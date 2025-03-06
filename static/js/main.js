/**
 * Main JavaScript file for H_Latex Web Application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Copy Button Functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    if (copyButtons.length > 0) {
        copyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');
                const textToCopy = document.getElementById(targetId).value || document.getElementById(targetId).textContent;
                
                // Copy to clipboard
                navigator.clipboard.writeText(textToCopy).then(() => {
                    // Temporarily change button text
                    const originalText = this.textContent;
                    this.textContent = 'Đã sao chép!';
                    
                    // Reset button text after 2 seconds
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 2000);
                }).catch(err => {
                    console.error('Could not copy text: ', err);
                    alert('Không thể sao chép văn bản. Vui lòng thử lại.');
                });
            });
        });
    }

    // LaTeX Render Buttons
    const renderButtons = document.querySelectorAll('.render-latex-btn');
    if (renderButtons.length > 0) {
        renderButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');
                const latexCode = document.getElementById(targetId).value || document.getElementById(targetId).textContent;
                const resultContainer = document.getElementById(this.getAttribute('data-result'));
                
                if (!latexCode) {
                    alert('Vui lòng nhập hoặc tạo mã LaTeX trước khi render!');
                    return;
                }
                
                // Show loading indicator
                resultContainer.innerHTML = `
                    <div class="spinner-container">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Đang xử lý...</span>
                        </div>
                        <div class="ms-3">Đang xử lý...</div>
                    </div>
                `;
                
                // Make request to render endpoint
                const endpoint = this.getAttribute('data-endpoint') || '/render';
                fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        latex_code: latexCode,
                        type: this.getAttribute('data-type') || 'standalone'
                    }),
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Lỗi khi render LaTeX');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    // Display PDF in an iframe
                    resultContainer.innerHTML = `
                        <div class="alert alert-success">Render thành công!</div>
                        <div class="d-flex justify-content-between mb-3">
                            <a href="${data.pdf_url}" target="_blank" class="btn btn-primary">Xem PDF</a>
                            <button type="button" class="btn btn-secondary" onclick="window.location.reload()">Tạo mới</button>
                        </div>
                        <iframe src="${data.pdf_url}" class="pdf-container" frameborder="0"></iframe>
                    `;
                })
                .catch(error => {
                    console.error('Error:', error);
                    resultContainer.innerHTML = `
                        <div class="alert alert-danger">
                            <h5>Lỗi khi render LaTeX</h5>
                            <p>${error.message}</p>
                        </div>
                    `;
                });
            });
        });
    }

    // Function Forms
    const functionForms = document.querySelectorAll('.function-form');
    if (functionForms.length > 0) {
        functionForms.forEach(form => {
            const functionType = form.querySelector('.function-type');
            if (functionType) {
                functionType.addEventListener('change', function() {
                    // Hide all parameter sections
                    const paramSections = form.querySelectorAll('.function-params');
                    paramSections.forEach(section => {
                        section.style.display = 'none';
                    });
                    
                    // Show selected function parameters
                    const selectedType = this.value;
                    const selectedParams = form.querySelector(`.function-params[data-type="${selectedType}"]`);
                    if (selectedParams) {
                        selectedParams.style.display = 'block';
                    }
                });
                
                // Trigger change event to show initial parameters
                functionType.dispatchEvent(new Event('change'));
            }
        });
    }

    // Input validation
    const numericInputs = document.querySelectorAll('input[type="number"], input[data-type="numeric"]');
    if (numericInputs.length > 0) {
        numericInputs.forEach(input => {
            input.addEventListener('input', function() {
                // Allow empty values
                if (this.value === '') return;
                
                // Remove non-numeric characters except decimal point, minus sign and fraction slash
                let value = this.value.replace(/[^0-9.\-\/]/g, '');
                
                // Ensure only one decimal point
                const decimalCount = (value.match(/\./g) || []).length;
                if (decimalCount > 1) {
                    const parts = value.split('.');
                    value = parts[0] + '.' + parts.slice(1).join('');
                }
                
                // Ensure only one fraction slash
                const slashCount = (value.match(/\//g) || []).length;
                if (slashCount > 1) {
                    const parts = value.split('/');
                    value = parts[0] + '/' + parts.slice(1).join('');
                }
                
                // Update value if changed
                if (this.value !== value) {
                    this.value = value;
                }
            });
        });
    }

    // Toggle sections
    const toggleButtons = document.querySelectorAll('.toggle-section');
    if (toggleButtons.length > 0) {
        toggleButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');
                const target = document.getElementById(targetId);
                
                if (target) {
                    // Toggle visibility
                    if (target.style.display === 'none') {
                        target.style.display = 'block';
                        this.innerHTML = this.innerHTML.replace('Hiện', 'Ẩn');
                    } else {
                        target.style.display = 'none';
                        this.innerHTML = this.innerHTML.replace('Ẩn', 'Hiện');
                    }
                }
            });
        });
    }

    // Custom file input
    const fileInputs = document.querySelectorAll('.custom-file-input');
    if (fileInputs.length > 0) {
        fileInputs.forEach(input => {
            input.addEventListener('change', function() {
                const fileLabel = this.nextElementSibling;
                if (fileLabel && this.files.length > 0) {
                    fileLabel.textContent = this.files[0].name;
                }
            });
        });
    }
});

/**
 * Utility function to format LaTeX code
 * @param {string} code - LaTeX code to format
 * @returns {string} - Formatted LaTeX code
 */
function formatLatexCode(code) {
    if (!code) return '';
    
    // Replace frac with dfrac
    code = code.replace(/\\frac/g, '\\dfrac');
    
    // Fix spacing around operators
    code = code.replace(/([^\\])([\+\-])/g, '$1 $2 ');
    
    // Remove multiple spaces
    code = code.replace(/\s+/g, ' ');
    
    // Format begin/end environments
    code = code.replace(/\\begin\{(\w+)\}/g, '\\begin{$1}\n');
    code = code.replace(/\\end\{(\w+)\}/g, '\n\\end{$1}');
    
    return code;
}

/**
 * Utility function to validate LaTeX code
 * @param {string} code - LaTeX code to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateLatexCode(code) {
    if (!code) return false;
    
    // Check for balanced braces
    let braceCount = 0;
    for (let i = 0; i < code.length; i++) {
        if (code[i] === '{') braceCount++;
        if (code[i] === '}') braceCount--;
        if (braceCount < 0) return false;
    }
    if (braceCount !== 0) return false;
    
    // Check for balanced begin/end statements
    const beginCount = (code.match(/\\begin\{/g) || []).length;
    const endCount = (code.match(/\\end\{/g) || []).length;
    if (beginCount !== endCount) return false;
    
    return true;
}
