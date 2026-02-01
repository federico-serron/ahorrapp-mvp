/**
 * Componente de Autenticación
 */

import { register, login } from '../api/client.js';
import { validateUsername, validatePassword, ValidationError } from '../utils/validator.js';
import { escapeHtml } from '../utils/sanitizer.js';

export class AuthComponent {
    constructor(containerId, onSuccess) {
        this.container = document.getElementById(containerId);
        this.onSuccess = onSuccess;
        this.isLoginMode = true;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Tab switching
        document.getElementById('tabLogin').addEventListener('click', () => this.switchMode(true));
        document.getElementById('tabRegister').addEventListener('click', () => this.switchMode(false));
        
        // Forms
        document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm').addEventListener('submit', (e) => this.handleRegister(e));
    }
    
    switchMode(isLogin) {
        this.isLoginMode = isLogin;
        
        // Actualizar tabs
        document.getElementById('tabLogin').classList.toggle('active', isLogin);
        document.getElementById('tabRegister').classList.toggle('active', !isLogin);
        
        // Mostrar/ocultar formularios
        document.getElementById('loginForm').classList.toggle('hidden', !isLogin);
        document.getElementById('registerForm').classList.toggle('hidden', isLogin);
        
        // Limpiar mensajes
        this.clearMessages();
    }
    
    async handleLogin(e) {
        e.preventDefault();
        
        try {
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            
            // Validar
            validateUsername(username);
            validatePassword(password);
            
            // Enviar
            const response = await login(username, password);
            
            // Guardar usuario en session storage
            sessionStorage.setItem('user', JSON.stringify(response));
            
            // Callback
            this.onSuccess(response);
            
        } catch (error) {
            this.showError(error.message, 'login');
        }
    }
    
    async handleRegister(e) {
        e.preventDefault();
        
        try {
            const username = document.getElementById('regUsername').value;
            const password = document.getElementById('regPassword').value;
            
            // Validar
            validateUsername(username);
            validatePassword(password);
            
            // Enviar
            await register(username, password);
            
            // Mostrar éxito
            this.showSuccess('Usuario creado! Inicia sesión', 'register');
            
            // Cambiar a login después de 1.5s
            setTimeout(() => this.switchMode(true), 1500);
            
        } catch (error) {
            this.showError(error.message, 'register');
        }
    }
    
    showError(message, form) {
        const messageDiv = document.getElementById(`${form}Message`);
        messageDiv.textContent = escapeHtml(message);
        messageDiv.className = 'message show error';
    }
    
    showSuccess(message, form) {
        const messageDiv = document.getElementById(`${form}Message`);
        messageDiv.textContent = escapeHtml(message);
        messageDiv.className = 'message show success';
    }
    
    clearMessages() {
        document.querySelectorAll('.message').forEach(msg => {
            msg.classList.remove('show');
        });
    }
    
    hide() {
        this.container.classList.add('hidden');
    }
    
    show() {
        this.container.classList.remove('hidden');
    }
}
