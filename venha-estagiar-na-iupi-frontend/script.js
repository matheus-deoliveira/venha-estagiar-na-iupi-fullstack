// ESTADO GLOBAL

const API_URL = 'http://127.0.0.1:8000/api/transactions/';

const USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NTk4MDE5LCJpYXQiOjE3NjQ1OTQ0MTksImp0aSI6Ijc2ODliMzgwN2Y4YzQ1YjlhMGQ4NmUxNmI5NWMxNTk3IiwidXNlcl9pZCI6IjEifQ.SfB0rUgpVlE4j7Oclp0lNe3DmmOUSZ6RqJGvkBKBRGE"

let currentTransactions = [];

// SELETORES DO DOM

const LIST_ELEMENT = document.getElementById('transactions-list');
const THEME_SWITCHER_BTN = document.getElementById('theme-switcher');
const FORM = document.getElementById('transaction-form');
const SEARCH_INPUT = document.getElementById('search-filter');
const SORT_SELECT = document.getElementById('sort-order');

// FUNÇÕES AUXILIARES 

/**
 * Formata um valor numérico para o padrão de moeda Real Brasileiro (BRL).
 * @param {number} value - O valor a ser formatado.
 * @returns {string} String formatada (ex: R$ 1.500,00).
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Formata uma string de data (YYYY-MM-DD) para o padrão brasileiro (DD/MM/YYYY).
 * @param {Date} dateString - A data a ser formatada.
 * @returns {Date} A data formata (DD/MM/YYYY)
 */
function formatDate(dateString) {
    if(!dateString) return 'Data Inválida'; 
    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year}`;
}

/**
 * Limpa a lista atual e renderiza os itens recebidos no HTML.
 */
function renderList(transactions) {
    LIST_ELEMENT.innerHTML = '';

    transactions.forEach(transaction => {
        const li = document.createElement('li');
        li.classList.add('transaction-item', transaction.type);

        // Criei uma div 'right-side' para agrupar Valor e Botão
        li.innerHTML = `
            <div class="transaction-info">
                <h3>${transaction.description}</h3>
                <p>${formatDate(transaction.date)}</p>
            </div>
            
            <div class="right-side">
                <div class="transaction-amount">
                    ${transaction.type === 'expense' ? '-' : '+'} 
                    ${formatCurrency(transaction.amount)}
                </div>
                <button class="delete-btn" data-id="${transaction.id}" aria-label="Excluir Transação">
                    &times;
                </button>
            </div>
        `;

        LIST_ELEMENT.appendChild(li);
    });
}

/**
 * Filtra e Ordena antes de renderizar.
 * Deve ser usada sempre que os dados mudarem ou o usuário filtrar.
 */
function updateList() {
    // Pegar os valores dos inputs
    const searchTerm = SEARCH_INPUT.value.toLowerCase();
    const sortType = SORT_SELECT.value;

    // Filtra
    let filteredTransactions = currentTransactions.filter(transaction => {
        const description = transaction.description.toLowerCase();
        return description.includes(searchTerm);
    });

    // Ordena
    filteredTransactions.sort((a, b) => {
        if (sortType === 'date-desc') return new Date(b.date) - new Date(a.date);
        if (sortType === 'date-asc') return new Date(a.date) - new Date(b.date);
        if (sortType === 'amount-desc') return b.amount - a.amount;
        if (sortType === 'amount-asc') return a.amount - b.amount;
    });

    // Renderizar a lista final processada
    renderList(filteredTransactions);
}

/**
 * Salva a lista atual no LocalStorage para não perder ao recarregar.
 */
function saveToLocalStorage() {
    localStorage.setItem('transactions', JSON.stringify(currentTransactions));
}

async function loadTransactions() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/transactions/', {
            // Se tiver autenticação, lembre do Header aqui:
            headers: {
                'Authorization': `Bearer ${USER_TOKEN}`,
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        // Se tiver paginação (results), usa o results. Se não, usa o data direto.
        if (data.results) {
            currentTransactions = data.results;
        } else {
            currentTransactions = data;
        }

        updateList(); // Agora vai funcionar porque currentTransactions é uma lista array

    } catch (error) {
        console.error("Erro ao carregar:", error);
    }
}

async function loadSummary() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/summary/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${USER_TOKEN}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            alert("Sessão expirada. Faça login novamente.");
            return;
        }

        const data = await response.json();
        
        updateDisplay('total-balance', data.net_balance);

    } catch (error) {
        console.error("Erro ao carregar resumo:", error);
    }
}

// Função auxiliar para formatar dinheiro bonito (R$)
function updateDisplay(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        const numberValue = parseFloat(value || 0);
        
        element.innerText = numberValue.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
        
        if (elementId === 'total-balance') {
            element.classList.remove('positive', 'negative');
            if (numberValue >= 0) {
                element.classList.add('positive');
                element.style.color = ''; // Remove cor inline se tiver CSS de classe
            } else {
                element.classList.add('negative');
                element.style.color = ''; 
            }
        }
    }
}

// EVENTOS

FORM.addEventListener('submit', async (event) => {
    event.preventDefault();

    const description = document.getElementById('description').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const date = document.getElementById('date').value;
    const type = document.getElementById('type').value;

    const newTransaction = {
        description: description,
        amount: amount,
        date: date,
        type: type
    };

    try {
        // Envia para o Backend (POST)
        const response = await fetch(`${API_URL}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${USER_TOKEN}`
            },
            body: JSON.stringify(newTransaction)
        });

        if (response.ok) {
            // Se deu certo, recarrega a lista do servidor para garantir sincronia
            loadTransactions(); 
            loadSummary();
            FORM.reset();
        } else {
            alert('Erro ao salvar transação');
        }

    } catch (error) {
        console.error('Erro na requisição:', error);
    }
});

// FUNÇÃO DE EXCLUIR

LIST_ELEMENT.addEventListener('click', async (event) => {
    const deleteButton = event.target.closest('.delete-btn');
    if (!deleteButton) return;

    const idToDelete = deleteButton.dataset.id;

    const confirmDelete = confirm('Tem certeza que deseja excluir?');
    if (!confirmDelete) return;

    try {
        // Envia para o Backend (DELETE)
        // Ex: http://127.0.0.1:8000/api/transactions/15
        const response = await fetch(`${API_URL}${idToDelete}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${USER_TOKEN}`
            }
        });

        if (response.ok) {
            loadTransactions(); // Recarrega a lista atualizada
            loadSummary();
        } else {
            alert('Erro ao excluir.');
        }

    } catch (error) {
        console.error('Erro ao excluir:', error);
    }
});

// Filtros e Ordenação
SEARCH_INPUT.addEventListener('input', updateList);
SORT_SELECT.addEventListener('change', updateList);

// Verificar se já existe um tema salvo
const savedTheme = localStorage.getItem('theme');

// Se o tema salvo for 'dark', ativa ele imediatamente
if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
}

// Tema Dark/Light
if (THEME_SWITCHER_BTN) {
    THEME_SWITCHER_BTN.addEventListener('click', () => {
        // Alterna a classe no body
        document.body.classList.toggle('dark-mode');

        // Verifica se ficou escuro ou claro
        const isDark = document.body.classList.contains('dark-mode');

        // Salva a preferência no navegador
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
}

// INICIALIZAÇÃO

/**
 * Função de inicialização da aplicação. A "main"
 */
function init() {
    loadTransactions();
    loadSummary();
}

// Inicia a aplicação
init();
