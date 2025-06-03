/**
 * JavaScript для работы с блокчейн-функционалом на странице токена
 */

document.addEventListener('DOMContentLoaded', function() {
    // Контейнер для блокчейн-информации
    const walletInfoContainer = document.getElementById('wallet-info-container');
    const tokenBalanceElement = document.getElementById('token-balance');
    const connectWalletButton = document.getElementById('connect-wallet-btn');
    
    // Проверяем, есть ли MetaMask
    const isMetaMaskInstalled = typeof window.ethereum !== 'undefined';
    
    // Обработчик для кнопки подключения кошелька
    if (connectWalletButton) {
        connectWalletButton.addEventListener('click', async function() {
            if (!isMetaMaskInstalled) {
                alert('Пожалуйста, установите MetaMask!');
                window.open('https://metamask.io/download.html', '_blank');
                return;
            }
            
            try {
                // Подключаем кошелек
                const account = await connectWallet();
                
                // Обновляем интерфейс
                connectWalletButton.textContent = account.substring(0, 6) + '...' + account.substring(38);
                connectWalletButton.classList.remove('btn-primary');
                connectWalletButton.classList.add('btn-success');
                
                // Показываем информацию о кошельке
                walletInfoContainer.style.display = 'block';
                
                // Получаем баланс токенов, если указан адрес контракта
                const tokenAddress = document.getElementById('token-address').value;
                if (tokenAddress) {
                    const balance = await getTokenBalance(tokenAddress, account);
                    if (tokenBalanceElement) {
                        tokenBalanceElement.textContent = balance;
                    }
                }
                
                // Сохраняем адрес кошелька в форму для отправки на сервер
                const walletInputs = document.querySelectorAll('.wallet-address-input');
                walletInputs.forEach(input => {
                    input.value = account;
                });
                
                // Эвент для других скриптов
                document.dispatchEvent(new CustomEvent('walletConnected', {
                    detail: { address: account }
                }));
            } catch (error) {
                console.error("Ошибка при подключении кошелька:", error);
                if (error.code === "NO_METAMASK") {
                    alert('Пожалуйста, установите MetaMask!');
                    window.open('https://metamask.io/download.html', '_blank');
                } else if (error.code === 4001) {
                    alert('Вы отклонили подключение кошелька.');
                } else {
                    alert('Произошла ошибка при подключении кошелька: ' + error.message);
                }
            }
        });
    }
    
    // Автоматическое подключение кошелька, если он уже был подключен
    async function autoConnectWallet() {
        if (isMetaMaskInstalled && connectWalletButton) {
            try {
                const accounts = await ethereum.request({ method: 'eth_accounts' });
                if (accounts.length > 0) {
                    const account = accounts[0];
                    
                    // Обновляем интерфейс
                    connectWalletButton.textContent = account.substring(0, 6) + '...' + account.substring(38);
                    connectWalletButton.classList.remove('btn-primary');
                    connectWalletButton.classList.add('btn-success');
                    
                    // Показываем информацию о кошельке
                    if (walletInfoContainer) {
                        walletInfoContainer.style.display = 'block';
                    }
                    
                    // Получаем баланс токенов, если указан адрес контракта
                    const tokenAddressElement = document.getElementById('token-address');
                    if (tokenAddressElement && tokenBalanceElement) {
                        const tokenAddress = tokenAddressElement.value;
                        if (tokenAddress) {
                            const balance = await getTokenBalance(tokenAddress, account);
                            tokenBalanceElement.textContent = balance;
                        }
                    }
                    
                    // Заполняем поля с адресом кошелька
                    const walletInputs = document.querySelectorAll('.wallet-address-input');
                    walletInputs.forEach(input => {
                        input.value = account;
                    });
                    
                    // Эвент для других скриптов
                    document.dispatchEvent(new CustomEvent('walletConnected', {
                        detail: { address: account }
                    }));
                }
            } catch (error) {
                console.error("Ошибка при автоматическом подключении кошелька:", error);
            }
        }
    }
    
    // Попытка автоматического подключения кошелька
    autoConnectWallet();
});
