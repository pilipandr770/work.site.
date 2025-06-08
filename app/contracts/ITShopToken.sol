// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title ITShopToken
 * @dev Контракт ERC20 токена для проекта IT магазина с дополнительными функциями для токенсейла и DAO
 */
contract ITShopToken {
    // Стандартные переменные ERC20
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    // Отображение балансов и разрешений
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    // События
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    // Владелец контракта
    address public owner;
    
    // Сумма токенов, заблокированных для аирдропа и токенсейла
    uint256 public airdropReserve;
    uint256 public tokenSaleReserve;
    
    // DAO переменные
    struct Proposal {
        uint256 id;
        string description;
        uint256 startTime;
        uint256 endTime;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        mapping(address => bool) voted;
    }
    
    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    
    // Модификаторы
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    /**
     * @dev Конструктор, устанавливающий начальные значения токена
     * @param _name Название токена
     * @param _symbol Символ токена
     * @param _initialSupply Начальное предложение токена (в наименьших единицах)
     */
    constructor(string memory _name, string memory _symbol, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _initialSupply;
        owner = msg.sender;
        
        // Выделяем 30% токенов для аирдропа и токенсейла
        airdropReserve = _initialSupply * 10 / 100; // 10% для аирдропа
        tokenSaleReserve = _initialSupply * 20 / 100; // 20% для токенсейла
        
        // Оставшиеся 70% идут владельцу контракта
        balanceOf[msg.sender] = _initialSupply - airdropReserve - tokenSaleReserve;
        
        // Выделяем резервы для аирдропа и токенсейла
        balanceOf[address(this)] = airdropReserve + tokenSaleReserve;
        
        emit Transfer(address(0), msg.sender, balanceOf[msg.sender]);
        emit Transfer(address(0), address(this), balanceOf[address(this)]);
    }
    
    /**
     * @dev Передача токенов
     * @param _to Адрес получателя
     * @param _value Количество токенов для передачи
     * @return Успешность операции
     */
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "Transfer to zero address");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    
    /**
     * @dev Утверждение расходования токенов от имени владельца
     * @param _spender Адрес, которому разрешается тратить токены
     * @param _value Количество разрешенных к расходованию токенов
     * @return Успешность операции
     */
    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    
    /**
     * @dev Передача токенов от имени другого адреса
     * @param _from Адрес отправителя
     * @param _to Адрес получателя
     * @param _value Количество токенов для передачи
     * @return Успешность операции
     */
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "Transfer to zero address");
        require(balanceOf[_from] >= _value, "Insufficient balance");
        require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");
        
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
    
    // Функции для аирдропа и токенсейла
    
    /**
     * @dev Отправка токенов для аирдропа
     * @param _recipients Массив адресов получателей
     * @param _values Массив количеств токенов для каждого получателя
     * @return Успешность операции
     */
    function airdrop(address[] memory _recipients, uint256[] memory _values) public onlyOwner returns (bool) {
        require(_recipients.length == _values.length, "Arrays must have same length");
        
        uint256 totalAmount = 0;
        for (uint256 i = 0; i < _values.length; i++) {
            totalAmount += _values[i];
        }
        
        require(totalAmount <= airdropReserve, "Exceeds airdrop reserve");
        
        for (uint256 i = 0; i < _recipients.length; i++) {
            balanceOf[address(this)] -= _values[i];
            balanceOf[_recipients[i]] += _values[i];
            emit Transfer(address(this), _recipients[i], _values[i]);
        }
        
        airdropReserve -= totalAmount;
        return true;
    }
    
    /**
     * @dev Продажа токенов
     * @param _buyer Адрес покупателя
     * @param _amount Количество покупаемых токенов
     * @return Успешность операции
     */
    function tokenSale(address _buyer, uint256 _amount) public onlyOwner returns (bool) {
        require(_amount <= tokenSaleReserve, "Exceeds token sale reserve");
        
        balanceOf[address(this)] -= _amount;
        balanceOf[_buyer] += _amount;
        tokenSaleReserve -= _amount;
        
        emit Transfer(address(this), _buyer, _amount);
        return true;
    }
    
    // Функции DAO
    
    /**
     * @dev Создание нового предложения
     * @param _description Описание предложения
     * @param _durationHours Продолжительность голосования в часах
     * @return ID созданного предложения
     */
    function createProposal(string memory _description, uint256 _durationHours) public returns (uint256) {
        require(balanceOf[msg.sender] >= 100 * 10**decimals, "Need at least 100 tokens to create proposal");
        
        proposalCount++;
        Proposal storage proposal = proposals[proposalCount];
        proposal.id = proposalCount;
        proposal.description = _description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + (_durationHours * 1 hours);
        
        return proposalCount;
    }
    
    /**
     * @dev Голосование по предложению
     * @param _proposalId ID предложения
     * @param _voteYes true для голоса "за", false для голоса "против"
     */
    function vote(uint256 _proposalId, bool _voteYes) public {
        require(_proposalId > 0 && _proposalId <= proposalCount, "Invalid proposal ID");
        Proposal storage proposal = proposals[_proposalId];
        
        require(block.timestamp >= proposal.startTime, "Voting not started");
        require(block.timestamp < proposal.endTime, "Voting ended");
        require(!proposal.voted[msg.sender], "Already voted");
        
        uint256 voteWeight = balanceOf[msg.sender];
        require(voteWeight > 0, "No voting power");
        
        proposal.voted[msg.sender] = true;
        
        if (_voteYes) {
            proposal.yesVotes += voteWeight;
        } else {
            proposal.noVotes += voteWeight;
        }
    }
    
    /**
     * @dev Выполнение принятого предложения
     * @param _proposalId ID предложения
     */
    function executeProposal(uint256 _proposalId) public onlyOwner {
        require(_proposalId > 0 && _proposalId <= proposalCount, "Invalid proposal ID");
        Proposal storage proposal = proposals[_proposalId];
        
        require(block.timestamp >= proposal.endTime, "Voting not ended");
        require(!proposal.executed, "Already executed");
        require(proposal.yesVotes > proposal.noVotes, "Proposal rejected");
        
        proposal.executed = true;
        
        // Логика выполнения предложения должна быть реализована отдельно
        // Здесь может быть вызов внешнего контракта или другая логика
    }
    
    /**
     * @dev Получение информации о предложении
     * @param _proposalId ID предложения
     * @return description Описание предложения
     * @return startTime Время начала голосования
     * @return endTime Время окончания голосования
     * @return yesVotes Количество голосов "за"
     * @return noVotes Количество голосов "против"
     * @return executed Выполнено ли предложение
     */
    function getProposal(uint256 _proposalId) public view returns (
        string memory description,
        uint256 startTime,
        uint256 endTime,
        uint256 yesVotes,
        uint256 noVotes,
        bool executed
    ) {
        require(_proposalId > 0 && _proposalId <= proposalCount, "Invalid proposal ID");
        Proposal storage proposal = proposals[_proposalId];
        
        return (
            proposal.description,
            proposal.startTime,
            proposal.endTime,
            proposal.yesVotes,
            proposal.noVotes,
            proposal.executed
        );
    }
}
