/**
 * Утилиты для работы с Web3 и блокчейном
 */

// Настройки сети Polygon
const POLYGON_TESTNET_CONFIG = {
    chainId: '0x13881', // 80001 для Mumbai Testnet
    chainName: 'Polygon Mumbai Testnet',
    nativeCurrency: {
        name: 'MATIC',
        symbol: 'MATIC',
        decimals: 18
    },
    rpcUrls: ['https://rpc-mumbai.maticvigil.com/'],
    blockExplorerUrls: ['https://mumbai.polygonscan.com/']
};

// === Налаштування для Polygon Mainnet ===
const POLYGON_MAINNET_CONFIG = {
    chainId: '0x89', // 137 для Polygon Mainnet
    chainName: 'Polygon Mainnet',
    nativeCurrency: {
        name: 'MATIC',
        symbol: 'MATIC',
        decimals: 18
    },
    rpcUrls: ['https://polygon-rpc.com/'],
    blockExplorerUrls: ['https://polygonscan.com/']
};

// Подключение к MetaMask (Polygon Mainnet)
async function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];
            await switchToPolygonMainnet();
            return account;
        } catch (error) {
            console.error("Ошибка подключения к MetaMask:", error);
            throw error;
        }
    } else {
        const error = new Error("Пожалуйста, установите MetaMask!");
        error.code = "NO_METAMASK";
        throw error;
    }
}

// Переключение на Polygon Mainnet
async function switchToPolygonMainnet() {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: POLYGON_MAINNET_CONFIG.chainId }],
        });
    } catch (error) {
        if (error.code === 4902) {
            try {
                await window.ethereum.request({
                    method: 'wallet_addEthereumChain',
                    params: [POLYGON_MAINNET_CONFIG],
                });
            } catch (addError) {
                console.error("Ошибка добавления сети Polygon Mainnet:", addError);
                throw addError;
            }
        } else {
            console.error("Ошибка переключения на сеть Polygon Mainnet:", error);
            throw error;
        }
    }
}

// Получение баланса токена
async function getTokenBalance(tokenAddress, walletAddress) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const tokenContract = new ethers.Contract(
        tokenAddress,
        [
            "function balanceOf(address account) external view returns (uint256)",
            "function decimals() external view returns (uint8)"
        ],
        provider
    );
    
    try {
        const decimals = await tokenContract.decimals();
        const balance = await tokenContract.balanceOf(walletAddress);
        return ethers.utils.formatUnits(balance, decimals);
    } catch (error) {
        console.error("Ошибка получения баланса токена:", error);
        throw error;
    }
}

// Покупка токенов (для токенсейла)
async function purchaseTokens(tokenSaleAddress, amount) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const tokenSaleContract = new ethers.Contract(
        tokenSaleAddress,
        [
            "function buyTokens(uint256 amount) external payable"
        ],
        signer
    );
    
    try {
        // Отправляем транзакцию покупки токенов
        const tx = await tokenSaleContract.buyTokens(
            ethers.utils.parseUnits(amount.toString(), 18),
            { value: ethers.utils.parseEther("0.01") } // Пример стоимости
        );
        
        // Ждем подтверждения транзакции
        const receipt = await tx.wait();
        return receipt.transactionHash;
    } catch (error) {
        console.error("Ошибка покупки токенов:", error);
        throw error;
    }
}

// Оплата заказа токенами
async function payWithTokens(tokenAddress, recipientAddress, amount, orderId) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const tokenContract = new ethers.Contract(
        tokenAddress,
        [
            "function transfer(address recipient, uint256 amount) external returns (bool)"
        ],
        signer
    );
    
    try {
        // Отправляем транзакцию перевода токенов
        const tx = await tokenContract.transfer(
            recipientAddress,
            ethers.utils.parseUnits(amount.toString(), 18)
        );
        
        // Ждем подтверждения транзакции
        const receipt = await tx.wait();
        
        // Обновляем статус заказа на сервере
        await fetch('/api/token/transfer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                order_id: orderId,
                tx_hash: receipt.transactionHash
            })
        });
        
        return receipt.transactionHash;
    } catch (error) {
        console.error("Ошибка оплаты токенами:", error);
        throw error;
    }
}

// Голосование в DAO
async function voteInDao(daoContractAddress, proposalId, voteFor) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const daoContract = new ethers.Contract(
        daoContractAddress,
        [
            "function vote(uint256 proposalId, bool support) external"
        ],
        signer
    );
    
    try {
        // Отправляем транзакцию голосования
        const tx = await daoContract.vote(proposalId, voteFor);
        
        // Ждем подтверждения транзакции
        const receipt = await tx.wait();
        return receipt.transactionHash;
    } catch (error) {
        console.error("Ошибка голосования в DAO:", error);
        throw error;
    }
}

// Создание предложения в DAO
async function createDaoProposal(daoContractAddress, description) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const daoContract = new ethers.Contract(
        daoContractAddress,
        [
            "function propose(string memory description) external returns (uint256)"
        ],
        signer
    );
    
    try {
        // Отправляем транзакцию создания предложения
        const tx = await daoContract.propose(description);
        
        // Ждем подтверждения транзакции
        const receipt = await tx.wait();
        return receipt.transactionHash;
    } catch (error) {
        console.error("Ошибка создания предложения DAO:", error);
        throw error;
    }
}
