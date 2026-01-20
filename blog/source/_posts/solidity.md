---
title: solidity
date: 2024-10-25 08:45:51
category: web3
tags: course
created: 2026-01-18T12:49
updated: 2024-10-25 08:45:51
---

# Solidity代码块
真不想写这个啊，没见过的代码，直接搜的到时候背就行,一下代码都是Solidity代码块，为了便于查看用的是c++格式解析，因为sd根本就没有自带解析，也懒得找了

## 完成加减运算
int / uint ：分别表示有符号和无符号的不同位数的整型变量。 支持关键字 uint8 到 uint256 （无符号，从 8 位到 256 位）以及 int8 到 int256，以 8 位为步长递增。 uint 和 int 分别是 uint256 和 int256 的别名
```c++
pragma solidity >=0.4.21 <=0.8.0

contract MatchTest{
    function add(uint i,uint j) pure public returns(uint){
        return i + j;
    }
    function sub(uint i,uint j) pure public returns(uint){
        return i - j;
    }
}
```
你看连识别都用不了

## 简单计算器合约
题目: 创建一个合约，用于存储一个整数。用户可以通过 set(uint256 x) 函数来设置这个整数，通过 get() 函数来查询当前存储的值。

提示:
•    set(uint256 x)：设置存储的整数值。
•    get()：返回当前存储的整数值
题目: 实现一个简单的计算器合约，支持加法、减法、乘法和除法操作。分别实现 add(uint256 a, uint256 b)、subtract(uint256 a, uint256 b)、multiply(uint256 a, uint256 b) 和 divide(uint256 a, uint256 b) 函数。
提示:
add(uint256 a, uint256 b)：返回 a 和 b 的和。
subtract(uint256 a, uint256 b)：返回 a 和 b 的差。
multiply(uint256 a, uint256 b)：返回 a 和 b 的积。
divide(uint256 a, uint256 b)：返回 a 除以 b 的商，需检查 b 是否为零。
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleCalculator {
    // 加法函数
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    // 减法函数
    function subtract(uint256 a, uint256 b) public pure returns (uint256) {
        require(a >= b, "Subtraction would result in a negative value");
        return a - b;
    }

    // 乘法函数
    function multiply(uint256 a, uint256 b) public pure returns (uint256) {
        return a * b;
    }

    // 除法函数
    function divide(uint256 a, uint256 b) public pure returns (uint256) {
        require(b != 0, "Cannot divide by zero");
        return a / b;
    }
}
```

## 存储合约
题目: 创建一个合约，用于存储一个整数。用户可以通过 set(uint256 x) 函数来设置这个整数，通过 get() 函数来查询当前存储的值。

提示:
•    set(uint256 x)：设置存储的整数值。
•    get()：返回当前存储的整数值。
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private storedValue;

    // 设置存储的整数值
    function set(uint256 x) public {
        storedValue = x;
    }

    // 返回当前存储的整数值
    function get() public view returns (uint256) {
        return storedValue;
    }
}
``` 

## 简单身份验证合约
题目: 实现一个身份验证合约，允许用户注册和查询注册状态。用户可以通过 register() 函数注册，通过 isRegistered(address user) 函数查询某个地址是否已注册。

提示:
•    register()：用户调用此函数进行注册。
•    isRegistered(address user)：返回指定地址的注册状态。
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Authentication {
    mapping(address => bool) private registeredUsers;

    // 注册函数：调用该函数的用户地址将被标记为已注册
    function register() public {
        require(!registeredUsers[msg.sender], "User is already registered");
        registeredUsers[msg.sender] = true;
    }

    // 查询注册状态函数：返回指定地址的注册状态
    function isRegistered(address user) public view returns (bool) {
        return registeredUsers[user];
    }
}
```

## 简单拍卖合约
题目: 创建一个简单的拍卖合约，允许用户出价。实现 bid() 函数来提交出价，使用 getHighestBid() 函数查询当前最高出价。
提示:
•    bid()：提交出价，需确保出价高于当前最高出价。
•    getHighestBid()：返回当前最高出价。

```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleAuction {
    address public highestBidder;
    uint256 public highestBid;

    // 提交出价函数，要求新出价高于当前最高出价
    function bid() public payable {
        require(msg.value > highestBid, "Bid must be higher than the current highest bid");

        // 如果有之前的最高出价，将其退还给之前的最高出价者
        if (highestBidder != address(0)) {
            payable(highestBidder).transfer(highestBid);
        }

        // 更新最高出价者和最高出价
        highestBidder = msg.sender;
        highestBid = msg.value;
    }

    // 查询当前最高出价
    function getHighestBid() public view returns (uint256) {
        return highestBid;
    }
}
```

## 简单奖励合约
题目: 创建一个合约，允许用户存款并根据存款金额给予奖励。实现 deposit() 函数进行存款和 getReward() 函数查询奖励。

提示:
•    deposit()：存入以太，系统给予 10% 的奖励。
•    getReward()：查询当前用户的奖励。
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DepositRewards {
    mapping(address => uint256) private deposits;
    mapping(address => uint256) private rewards;

    // 存款函数，用户存入以太并获得 10% 的奖励
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");

        // 记录用户的存款金额
        deposits[msg.sender] += msg.value;

        // 计算奖励并更新奖励映射
        uint256 reward = (msg.value * 10) / 100;
        rewards[msg.sender] += reward;
    }

    // 查询当前用户的奖励
    function getReward() public view returns (uint256) {
        return rewards[msg.sender];
    }
}
```

## 投票合约
题目: 创建一个投票合约，允许用户注册候选人并为其投票。实现 addCandidate(string memory name) 和 vote(uint candidateId) 函数。

提示:
•    addCandidate(string memory name)：添加新的候选人。
•    vote(uint candidateId)：为指定候选人投票。
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        string name;
        uint256 voteCount;
    }

    Candidate[] public candidates;
    mapping(address => bool) private hasVoted;

    // 添加候选人函数
    function addCandidate(string memory name) public {
        candidates.push(Candidate(name, 0));
    }

    // 投票函数，为指定候选人投票
    function vote(uint256 candidateId) public {
        require(candidateId < candidates.length, "Invalid candidate ID");
        require(!hasVoted[msg.sender], "You have already voted");

        // 增加候选人的票数
        candidates[candidateId].voteCount += 1;

        // 标记该用户已投票
        hasVoted[msg.sender] = true;
    }

    // 获取候选人总数
    function getCandidateCount() public view returns (uint256) {
        return candidates.length;
    }

    // 获取候选人信息
    function getCandidate(uint256 candidateId) public view returns (string memory, uint256) {
        require(candidateId < candidates.length, "Invalid candidate ID");
        return (candidates[candidateId].name, candidates[candidateId].voteCount);
    }
}
```

## 众筹合约
题目: 创建一个众筹合约，允许用户出资并达到目标后提取资金。实现 contribute() 和 withdraw() 函数。

提示:
•    contribute()：允许用户捐款并记录贡献金额。
•    withdraw()：允许众筹目标达成后提取资金。
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Crowdfunding {
    address public owner;
    uint256 public goal;
    uint256 public totalContributions;
    bool public goalReached;
    
    mapping(address => uint256) public contributions;

    constructor(uint256 _goal) {
        owner = msg.sender;
        goal = _goal;
        goalReached = false;
    }

    // 出资函数，记录用户的贡献金额
    function contribute() public payable {
        require(msg.value > 0, "Contribution must be greater than zero");
        require(!goalReached, "Goal already reached");

        contributions[msg.sender] += msg.value;
        totalContributions += msg.value;

        // 如果总贡献金额达到或超过目标，标记为达成
        if (totalContributions >= goal) {
            goalReached = true;
        }
    }

    // 提取资金函数，众筹达成目标后允许合约所有者提取资金
    function withdraw() public {
        require(msg.sender == owner, "Only the owner can withdraw funds");
        require(goalReached, "Funding goal not reached");

        payable(owner).transfer(address(this).balance);
    }

    // 查询用户的贡献金额
    function getContribution(address contributor) public view returns (uint256) {
        return contributions[contributor];
    }
}
```

## 资产管理合约
题目: 开发一个合约，允许用户存款、取款并查询余额。实现 deposit()、withdraw(uint amount) 和 getBalance() 函数。

提示:
•    deposit()：存入以太。
•    withdraw(uint amount)：提取指定金额。
•    getBalance()：查询当前余额
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleBank {
    mapping(address => uint256) private balances;

    // 存款函数，将用户发送的以太存入他们的账户
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        balances[msg.sender] += msg.value;
    }

    // 取款函数，用户可以提取指定金额的以太
    function withdraw(uint256 amount) public {
        require(amount > 0, "Withdrawal amount must be greater than zero");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        // 更新余额并转账
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    // 查询当前余额
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}
```

## 合约升级示例
题目: 创建一个可升级的合约。初始合约实现 setValue(uint value) 和 getValue()，升级合约添加 incrementValue()。

提示:
•    setValue(uint value)：设置一个值。
•    getValue()：获取当前值。
•    incrementValue()：将当前值加一（在升级合约中实现）。
```c++
// SPDX-License-Identifier: MIT
//  可升级合约的代理合约
pragma solidity ^0.8.0;

contract Proxy {
    address public implementation;

    constructor(address _implementation) {
        implementation = _implementation;
    }

    function upgradeTo(address _implementation) public {
        implementation = _implementation;
    }

    fallback() external {
        address impl = implementation;
        require(impl != address(0), "Implementation not set");
        // 调用实现合约的方法
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            let size := returndatasize()
            returndatacopy(0, 0, size)
            switch result
            case 0 { revert(0, size) }
            default { return(0, size) }
        }
    }
}

// SPDX-License-Identifier: MIT
// 初始合约
pragma solidity ^0.8.0;

contract Initial {
    uint256 private value;

    function setValue(uint256 _value) public {
        value = _value;
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}

// SPDX-License-Identifier: MIT
// 升级合约
pragma solidity ^0.8.0;

import "./Initial.sol";

contract Upgraded is Initial {
    function incrementValue() public {
        value += 1;
    }
}
```

## 时间锁合约
题目: 实现一个时间锁合约，允许用户存入资金并设置锁定时间。实现 deposit(uint unlockTime) 和 withdraw() 函数。

提示:
•    deposit(uint unlockTime)：存入以太并设置解锁时间。
•    withdraw()：在解锁后提取资金
```c++
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeLock {
    struct Deposit {
        uint256 amount;
        uint256 unlockTime;
    }

    mapping(address => Deposit) private deposits;

    // 存入资金并设置解锁时间
    function deposit(uint256 unlockTime) public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        require(unlockTime > block.timestamp, "Unlock time must be in the future");

        // 更新用户存款信息
        deposits[msg.sender].amount += msg.value;
        deposits[msg.sender].unlockTime = unlockTime;
    }

    // 提取资金，只有在解锁后才允许
    function withdraw() public {
        Deposit storage userDeposit = deposits[msg.sender];
        require(block.timestamp >= userDeposit.unlockTime, "Funds are still locked");
        require(userDeposit.amount > 0, "No funds to withdraw");

        uint256 amountToWithdraw = userDeposit.amount;
        userDeposit.amount = 0; // 清空存款，避免重入攻击

        payable(msg.sender).transfer(amountToWithdraw);
    }

    // 查询当前用户的存款信息
    function getDepositInfo() public view returns (uint256 amount, uint256 unlockTime) {
        Deposit storage userDeposit = deposits[msg.sender];
        return (userDeposit.amount, userDeposit.unlockTime);
    }
}
```