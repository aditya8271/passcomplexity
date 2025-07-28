from flask import Flask, render_template_string

# Initialize the Flask application
app = Flask(__name__)

# The complete HTML, CSS, and JavaScript for the frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Checker</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {
            --bg-color-start: #0f172a;
            --bg-color-end: #1e293b;
            --card-color: rgba(30, 41, 59, 0.7);
            --text-color: #f1f5f9;
            --text-muted: #94a3b8;
            --border-color: rgba(148, 163, 184, 0.2);
            --accent-color: #38bdf8;
            
            /* Strength Colors */
            --strength-very-weak: #ef4444; /* red */
            --strength-weak: #f97316;      /* orange */
            --strength-medium: #facc15;     /* yellow */
            --strength-strong: #4ade80;     /* green */
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        @keyframes gradient-animation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(-45deg, var(--bg-color-start), var(--bg-color-end), #0f172a);
            background-size: 400% 400%;
            animation: gradient-animation 15s ease infinite;
            color: var(--text-color);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 1rem;
        }

        .container {
            width: 100%;
            max-width: 500px;
            background-color: var(--card-color);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            padding: 2.5rem;
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .header h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .header p { color: var(--text-muted); }

        .password-input-wrapper {
            position: relative;
            margin-bottom: 1rem;
        }

        #password-input {
            width: 100%;
            background-color: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.85rem 2.5rem 0.85rem 1rem;
            color: var(--text-color);
            font-size: 1rem;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        #password-input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.3);
        }

        .toggle-password {
            position: absolute;
            top: 50%;
            right: 1rem;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1.1rem;
        }
        
        .strength-meter-wrapper {
            margin-bottom: 1.5rem;
        }

        .strength-meter {
            height: 8px;
            width: 100%;
            background-color: rgba(15, 23, 42, 0.8);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .strength-bar {
            height: 100%;
            width: 0;
            background-color: var(--strength-very-weak);
            border-radius: 4px;
            transition: width 0.4s ease, background-color 0.4s ease;
        }

        .strength-label {
            text-align: right;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.5rem;
            height: 1.2em;
            color: var(--text-muted);
            transition: color 0.4s ease;
        }
        
        .criteria-list {
            list-style: none;
            padding: 0;
        }
        
        .criterion {
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
            color: var(--text-muted);
            transition: color 0.4s ease;
        }
        
        .criterion i {
            width: 20px;
            margin-right: 0.75rem;
            transition: all 0.4s ease;
            transform: scale(0.8);
            opacity: 0.7;
        }
        
        .criterion.met {
            color: var(--text-color);
        }
        
        .criterion.met i {
            color: var(--strength-strong);
            transform: scale(1);
            opacity: 1;
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Password Strength Checker</h1>
            <p>Enter a password to see how strong it is.</p>
        </div>
        
        <div class="password-input-wrapper">
            <input type="password" id="password-input" placeholder="Enter your password">
            <button class="toggle-password" id="toggle-password">
                <i class="fa-solid fa-eye"></i>
            </button>
        </div>
        
        <div class="strength-meter-wrapper">
            <div class="strength-meter">
                <div class="strength-bar" id="strength-bar"></div>
            </div>
            <div class="strength-label" id="strength-label"></div>
        </div>
        
        <ul class="criteria-list">
            <li class="criterion" id="length-criterion">
                <i class="fa-solid fa-circle-xmark"></i>
                <span>At least 8 characters long</span>
            </li>
            <li class="criterion" id="uppercase-criterion">
                <i class="fa-solid fa-circle-xmark"></i>
                <span>Contains an uppercase letter</span>
            </li>
            <li class="criterion" id="lowercase-criterion">
                <i class="fa-solid fa-circle-xmark"></i>
                <span>Contains a lowercase letter</span>
            </li>
            <li class="criterion" id="number-criterion">
                <i class="fa-solid fa-circle-xmark"></i>
                <span>Contains a number</span>
            </li>
            <li class="criterion" id="special-criterion">
                <i class="fa-solid fa-circle-xmark"></i>
                <span>Contains a special character (!@#$...)</span>
            </li>
        </ul>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const passwordInput = document.getElementById('password-input');
            const togglePasswordBtn = document.getElementById('toggle-password');
            const strengthBar = document.getElementById('strength-bar');
            const strengthLabel = document.getElementById('strength-label');
            
            const criteria = {
                length: document.getElementById('length-criterion'),
                uppercase: document.getElementById('uppercase-criterion'),
                lowercase: document.getElementById('lowercase-criterion'),
                number: document.getElementById('number-criterion'),
                special: document.getElementById('special-criterion')
            };

            const strengthLevels = {
                0: { text: "", color: "transparent" },
                1: { text: "Very Weak", color: "var(--strength-very-weak)" },
                2: { text: "Weak", color: "var(--strength-weak)" },
                3: { text: "Medium", color: "var(--strength-medium)" },
                4: { text: "Medium", color: "var(--strength-medium)" },
                5: { text: "Strong", color: "var(--strength-strong)" }
            };

            const checkPasswordStrength = () => {
                const password = passwordInput.value;
                let score = 0;

                // 1. Check length
                const isLengthMet = password.length >= 8;
                updateCriterion(criteria.length, isLengthMet);
                if (isLengthMet) score++;

                // 2. Check for uppercase letters
                const isUppercaseMet = /[A-Z]/.test(password);
                updateCriterion(criteria.uppercase, isUppercaseMet);
                if (isUppercaseMet) score++;

                // 3. Check for lowercase letters
                const isLowercaseMet = /[a-z]/.test(password);
                updateCriterion(criteria.lowercase, isLowercaseMet);
                if (isLowercaseMet) score++;

                // 4. Check for numbers
                const isNumberMet = /[0-9]/.test(password);
                updateCriterion(criteria.number, isNumberMet);
                if (isNumberMet) score++;

                // 5. Check for special characters
                const isSpecialMet = /[^A-Za-z0-9]/.test(password);
                updateCriterion(criteria.special, isSpecialMet);
                if (isSpecialMet) score++;
                
                // Update strength bar and label
                updateStrengthUI(score);
            };

            const updateCriterion = (element, isMet) => {
                const icon = element.querySelector('i');
                if (isMet) {
                    element.classList.add('met');
                    icon.classList.remove('fa-circle-xmark');
                    icon.classList.add('fa-circle-check');
                } else {
                    element.classList.remove('met');
                    icon.classList.remove('fa-circle-check');
                    icon.classList.add('fa-circle-xmark');
                }
            };
            
            const updateStrengthUI = (score) => {
                const level = strengthLevels[score] || strengthLevels[0];
                const width = (score / 5) * 100;
                
                if (passwordInput.value.length === 0) {
                    strengthBar.style.width = '0%';
                    strengthLabel.textContent = '';
                } else {
                    strengthBar.style.width = width + '%';
                    strengthBar.style.backgroundColor = level.color;
                    strengthLabel.textContent = level.text;
                    strengthLabel.style.color = level.color;
                }
            };

            const togglePasswordVisibility = () => {
                const icon = togglePasswordBtn.querySelector('i');
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    passwordInput.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            };

            passwordInput.addEventListener('input', checkPasswordStrength);
            togglePasswordBtn.addEventListener('click', togglePasswordVisibility);
            
            // Initial check in case of autofill
            checkPasswordStrength();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Renders the main page for the password checker."""
    # The logic is entirely client-side, so we just render the template.
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Run the Flask app, making it accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=False)
