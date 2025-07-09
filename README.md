# EstusFlask - E-commerce API

Uma API REST simples para e-commerce desenvolvida em Flask, implantada na AWS usando Elastic Beanstalk.

## 📋 Sobre o Projeto

Esta aplicação é uma API backend para um sistema de e-commerce que oferece funcionalidades de autenticação de usuários, gerenciamento de produtos e carrinho de compras. A API foi desenvolvida para ser consumida por aplicações frontend e está hospedada na AWS.

## 🛠️ Tecnologias Utilizadas

- **Flask 2.3.0** - Framework web principal
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-Login 0.6.2** - Gerenciamento de sessões de usuário
- **Flask-CORS 3.0.10** - Habilitação de CORS para requisições cross-origin
- **SQLite** - Banco de dados (via SQLAlchemy)

## 🏗️ Arquitetura e Padrões

- **Padrão MVC**: Separação clara entre modelos (User, Product, CartItem), rotas (controllers) e dados
- **RESTful API**: Endpoints seguindo convenções REST
- **ORM Pattern**: Uso do SQLAlchemy para abstração do banco de dados
- **Authentication Pattern**: Sistema de login baseado em sessões com Flask-Login

## 📦 Estrutura do Banco de Dados

### Modelos:
- **User**: Usuários do sistema com autenticação
- **Product**: Produtos disponíveis para compra
- **CartItem**: Itens no carrinho de cada usuário

## 🚀 Setup e Configuração

### Pré-requisitos
- Python 3.8+
- pip

### Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd EstusFlask
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python application.py
```

A API estará disponível em `http://localhost:5000`

### Configuração do Banco de Dados

O banco SQLite será criado automaticamente na primeira execução em `instance/ecommerce.db`.

## 📚 Endpoints Principais

### Autenticação
- `POST /login` - Login de usuário
- `POST /logout` - Logout de usuário

### Produtos
- `GET /api/products` - Listar todos os produtos
- `GET /api/products/<id>` - Obter produto específico
- `POST /api/products/add` - Adicionar produto (requer autenticação)
- `PUT /api/products/update/<id>` - Atualizar produto (requer autenticação)
- `DELETE /api/products/delete/<id>` - Deletar produto (requer autenticação)

### Carrinho
- `GET /api/cart` - Ver carrinho do usuário (requer autenticação)
- `POST /api/cart/add/<product_id>` - Adicionar ao carrinho (requer autenticação)
- `DELETE /api/cart/remove/<product_id>` - Remover do carrinho (requer autenticação)
- `POST /api/cart/checkout` - Finalizar compra (requer autenticação)

## ☁️ Deploy na AWS

Este projeto está configurado para deploy no **AWS Elastic Beanstalk**:

1. A aplicação principal está em `application.py` (nome requerido pelo Elastic Beanstalk)
2. As dependências estão listadas em `requirements.txt`
3. A configuração é compatível com o ambiente Python do Elastic Beanstalk

### Deploy:
```bash
# Instalar EB CLI (se necessário)
pip install awsebcli

# Inicializar aplicação EB
eb init

# Deploy
eb deploy
```

## 🔒 Segurança

- Autenticação baseada em sessões
- CORS habilitado para requisições cross-origin
- Senhas armazenadas em texto plano (⚠️ **Atenção**: Em produção, use hash de senhas)

## 📝 Notas de Desenvolvimento

- O projeto usa SQLite para desenvolvimento local
- Para produção, considere migrar para PostgreSQL ou MySQL
- Implemente hash de senhas antes do deploy em produção
- Configure variáveis de ambiente para informações sensíveis
