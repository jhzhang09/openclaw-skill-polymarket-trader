# OpenClaw Skill: Polymarket Trader

An autonomous trading skill for [OpenClaw](https://github.com/openclaw/openclaw) agents, enabling them to interact with the Polymarket prediction market platform.

[中文说明](#中文说明)

## Features

- **Balance Check**: Query USDC and collateral balances.
- **Market Search**: Find markets by ID or query (via external search integration).
- **Automated Trading**: Execute Buy/Sell orders via the CLOB (Central Limit Order Book) API.
- **Proxy Support**: Supports both EOA (Externally Owned Account) and Magic Link (Proxy) wallets.

## Installation

Clone this repository into your OpenClaw skills directory:

```bash
cd /root/clawd/skills
git clone https://github.com/jhzhang09/openclaw-skill-polymarket-trader.git polymarket-trader
```

## Configuration

Set the following environment variables in your OpenClaw agent's `.env` file or environment:

```bash
POLY_API_KEY=your_api_key
POLY_API_SECRET=your_api_secret
POLY_PASSPHRASE=your_passphrase
POLY_PROXY_ADDRESS=your_proxy_address_if_using_magic_link
```

## Usage

This skill exposes a `scripts/trader.py` script that can be called by the agent.

```bash
# Check balance
python3 scripts/trader.py balance

# Place an order (example)
python3 scripts/trader.py buy --market <ID> --outcome YES --amount 10
```

---

## <a id="中文说明"></a>中文说明

这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) Agent 设计的自动化交易技能，使其能够与 Polymarket 预测市场平台进行交互。

### 功能特性

- **余额查询**: 查询 USDC 余额和质押品余额。
- **市场搜索**: 通过 ID 或查询关键词查找市场。
- **自动交易**: 通过 CLOB (中央限价订单簿) API 执行买入/卖出订单。
- **代理支持**: 同时支持 EOA (外部拥有账户) 和 Magic Link (代理) 钱包。

### 安装

将此仓库克隆到您的 OpenClaw skills 目录中：

```bash
cd /root/clawd/skills
git clone https://github.com/jhzhang09/openclaw-skill-polymarket-trader.git polymarket-trader
```

### 配置

在您的 OpenClaw agent 的 `.env` 文件或环境变量中设置以下内容：

```bash
POLY_API_KEY=your_api_key
POLY_API_SECRET=your_api_secret
POLY_PASSPHRASE=your_passphrase
POLY_PROXY_ADDRESS=your_proxy_address_if_using_magic_link
```

### 使用方法

此技能提供了一个 `scripts/trader.py` 脚本，可供 Agent 调用。

```bash
# 查询余额
python3 scripts/trader.py balance

# 下单示例
python3 scripts/trader.py buy --market <ID> --outcome YES --amount 10
```

## License

MIT
