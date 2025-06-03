// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title ITShopToken
 * @dev ERC20 токен для экосистемы IT-магазина
 */
contract ITShopToken is ERC20, ERC20Burnable, Pausable, AccessControl {
    // Роли для управления контрактом
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant AIRDROP_ROLE = keccak256("AIRDROP_ROLE");
    
    // Максимальное количество токенов
    uint256 public constant MAX_SUPPLY = 1000000 * 10**18; // 1,000,000 токенов
    
    // События
    event AirdropDistribution(address indexed to, uint256 amount);
    event TokensBought(address indexed buyer, uint256 amount, uint256 paidAmount);
    
    // Конструктор
    constructor() ERC20("IT Shop Token", "ITST") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(AIRDROP_ROLE, msg.sender);
        
        // Создаем начальное предложение для команды и токенсейла
        _mint(msg.sender, 300000 * 10**18); // 300,000 токенов (30%)
    }
    
    // Функции для управления токеном
    
    /**
     * @dev Приостанавливает все трансферы токенов
     */
    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }
    
    /**
     * @dev Возобновляет все трансферы токенов
     */
    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }
    
    /**
     * @dev Создает новые токены и отправляет их на указанный адрес
     * Может быть вызвана только адресами с ролью MINTER_ROLE
     */
    function mint(address to, uint256 amount) public onlyRole(MINTER_ROLE) {
        require(totalSupply() + amount <= MAX_SUPPLY, "ITShopToken: Max supply exceeded");
        _mint(to, amount);
    }
    
    /**
     * @dev Распределяет токены для аирдропа
     * Может быть вызвана только адресами с ролью AIRDROP_ROLE
     */
    function airdrop(address[] calldata recipients, uint256[] calldata amounts) 
        external 
        onlyRole(AIRDROP_ROLE) 
    {
        require(recipients.length == amounts.length, "ITShopToken: Arrays length mismatch");
        
        uint256 totalAmount = 0;
        for (uint256 i = 0; i < amounts.length; i++) {
            totalAmount += amounts[i];
        }
        
        require(totalSupply() + totalAmount <= MAX_SUPPLY, "ITShopToken: Max supply exceeded");
        
        for (uint256 i = 0; i < recipients.length; i++) {
            _mint(recipients[i], amounts[i]);
            emit AirdropDistribution(recipients[i], amounts[i]);
        }
    }
    
    /**
     * @dev Функция для покупки токенов
     */
    function buyTokens(uint256 tokenAmount) external payable {
        require(msg.value > 0, "ITShopToken: Must send ETH to buy tokens");
        require(totalSupply() + tokenAmount <= MAX_SUPPLY, "ITShopToken: Max supply exceeded");
        
        // В реальном контракте здесь должна быть логика определения цены
        // Сейчас мы просто выпускаем токены отправителю
        _mint(msg.sender, tokenAmount);
        emit TokensBought(msg.sender, tokenAmount, msg.value);
    }
    
    /**
     * @dev Внутренний хук для проверки перед трансфером токенов
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
}

/**
 * @title TokenSale
 * @dev Контракт для проведения токенсейла
 */
contract TokenSale {
    ITShopToken public token;
    address public owner;
    
    uint256 public tokenPrice;         // Цена токена в wei
    uint256 public minPurchase;        // Минимальная покупка в токенах
    uint256 public maxPurchase;        // Максимальная покупка в токенах
    uint256 public tokensAvailable;    // Доступное количество токенов для продажи
    
    bool public isActive = false;      // Активен ли токенсейл
    
    // События
    event TokensPurchased(address indexed buyer, uint256 amount, uint256 cost);
    
    // Модификатор для ограничения доступа только владельцу
    modifier onlyOwner() {
        require(msg.sender == owner, "TokenSale: Caller is not the owner");
        _;
    }
    
    // Конструктор
    constructor(address tokenAddress, uint256 _tokenPrice, uint256 _minPurchase, uint256 _maxPurchase) {
        token = ITShopToken(tokenAddress);
        owner = msg.sender;
        tokenPrice = _tokenPrice;
        minPurchase = _minPurchase;
        maxPurchase = _maxPurchase;
    }
    
    /**
     * @dev Активирует токенсейл
     */
    function startSale(uint256 totalTokens) external onlyOwner {
        require(!isActive, "TokenSale: Sale is already active");
        require(totalTokens > 0, "TokenSale: Invalid token amount");
        
        tokensAvailable = totalTokens;
        isActive = true;
    }
    
    /**
     * @dev Останавливает токенсейл
     */
    function stopSale() external onlyOwner {
        require(isActive, "TokenSale: Sale is not active");
        isActive = false;
    }
    
    /**
     * @dev Функция для покупки токенов
     */
    function buyTokens(uint256 tokenAmount) external payable {
        require(isActive, "TokenSale: Sale is not active");
        require(tokenAmount >= minPurchase, "TokenSale: Below min purchase");
        require(tokenAmount <= maxPurchase, "TokenSale: Above max purchase");
        require(tokenAmount <= tokensAvailable, "TokenSale: Not enough tokens available");
        
        uint256 cost = tokenAmount * tokenPrice;
        require(msg.value >= cost, "TokenSale: Insufficient payment");
        
        // Обновляем доступное количество токенов
        tokensAvailable -= tokenAmount;
        
        // Возврат лишних средств, если таковые имеются
        if (msg.value > cost) {
            payable(msg.sender).transfer(msg.value - cost);
        }
        
        // Отправляем токены покупателю
        token.mint(msg.sender, tokenAmount);
        
        emit TokensPurchased(msg.sender, tokenAmount, cost);
    }
    
    /**
     * @dev Вывод средств с контракта
     */
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "TokenSale: No funds to withdraw");
        payable(owner).transfer(balance);
    }
}

/**
 * @title SimpleDAO
 * @dev Простой DAO контракт для голосований
 */
contract SimpleDAO {
    struct Proposal {
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        mapping(address => bool) hasVoted;
    }
    
    ITShopToken public token;
    address public owner;
    
    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    
    uint256 public minTokensToVote;  // Минимальное количество токенов для голосования
    
    // События
    event ProposalCreated(uint256 indexed proposalId, string description, uint256 startTime, uint256 endTime);
    event Voted(uint256 indexed proposalId, address indexed voter, bool support);
    event ProposalExecuted(uint256 indexed proposalId);
    
    // Модификатор для ограничения доступа только владельцу
    modifier onlyOwner() {
        require(msg.sender == owner, "SimpleDAO: Caller is not the owner");
        _;
    }
    
    // Конструктор
    constructor(address tokenAddress, uint256 _minTokensToVote) {
        token = ITShopToken(tokenAddress);
        owner = msg.sender;
        minTokensToVote = _minTokensToVote;
    }
    
    /**
     * @dev Создает новое предложение для голосования
     */
    function propose(string memory description) external returns (uint256) {
        require(token.balanceOf(msg.sender) >= minTokensToVote, "SimpleDAO: Not enough tokens");
        
        uint256 proposalId = proposalCount++;
        Proposal storage newProposal = proposals[proposalId];
        
        newProposal.description = description;
        newProposal.startTime = block.timestamp;
        newProposal.endTime = block.timestamp + 7 days;  // Голосование длится 7 дней
        
        emit ProposalCreated(proposalId, description, newProposal.startTime, newProposal.endTime);
        
        return proposalId;
    }
    
    /**
     * @dev Позволяет голосовать за или против предложения
     */
    function vote(uint256 proposalId, bool support) external {
        require(token.balanceOf(msg.sender) >= minTokensToVote, "SimpleDAO: Not enough tokens");
        
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp >= proposal.startTime, "SimpleDAO: Voting not started");
        require(block.timestamp <= proposal.endTime, "SimpleDAO: Voting ended");
        require(!proposal.hasVoted[msg.sender], "SimpleDAO: Already voted");
        
        if (support) {
            proposal.forVotes += token.balanceOf(msg.sender);
        } else {
            proposal.againstVotes += token.balanceOf(msg.sender);
        }
        
        proposal.hasVoted[msg.sender] = true;
        
        emit Voted(proposalId, msg.sender, support);
    }
    
    /**
     * @dev Выполняет предложение после голосования
     */
    function executeProposal(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        
        require(block.timestamp > proposal.endTime, "SimpleDAO: Voting not ended");
        require(!proposal.executed, "SimpleDAO: Already executed");
        
        proposal.executed = true;
        
        emit ProposalExecuted(proposalId);
        
        // Здесь должна быть логика выполнения предложения
        // В простом варианте мы только помечаем его как выполненное
    }
    
    /**
     * @dev Обновляет минимальное количество токенов для голосования
     */
    function setMinTokensToVote(uint256 _minTokensToVote) external onlyOwner {
        minTokensToVote = _minTokensToVote;
    }
}
