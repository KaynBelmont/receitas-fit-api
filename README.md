# FitChef AI 🥗

App inteligente de receitas fit que sugere receitas saudáveis com base nos ingredientes que você tem em casa, com modo de preparo completo e informações nutricionais.

## Funcionalidades

- Geração de 3 receitas fit personalizadas com base nos ingredientes informados
- Suporte a preferências alimentares (Low Carb, Vegano, Sem Glúten, Alta Proteína, etc.)
- Informações completas: tempo de preparo, porções, calorias e macros
- Dicas nutricionais para cada receita
- Sugestões de ingredientes organizadas por categoria
- Interface responsiva e moderna

## Tecnologias

**Backend**
- Python 3.11
- FastAPI
- OpenRouter API (LLM gratuito)
- Docker

**Frontend**
- React
- Tailwind CSS
- Lovable (deploy)

**Deploy**
- Backend: Render.com
- Frontend: Lovable

## Como rodar localmente

**Pré-requisitos:** Python 3.11+, Git

```bash
# Clone o repositório
git clone https://github.com/KaynBelmont/receitas-fit-api.git
cd receitas-fit-api

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
# Crie um arquivo .env na raiz com:
# OPENROUTER_API_KEY=sua_chave_aqui

# Rode o servidor
uvicorn main:app --reload
```

Acesse a documentação em `http://localhost:8000/docs`

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `OPENROUTER_API_KEY` | Chave da API do OpenRouter (gratuita em openrouter.ai) |

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Health check da API |
| POST | `/receitas` | Gera 3 receitas com base nos ingredientes |
| GET | `/ingredientes/sugestoes` | Retorna sugestões de ingredientes por categoria |

**Exemplo de requisição POST /receitas:**
```json
{
  "ingredientes": ["frango", "brócolis", "arroz integral"],
  "preferencias": "Alta Proteína"
}
```

## Deploy

O backend está hospedado no Render.com usando Docker com Python 3.11.
O frontend está hospedado no Lovable.

URL da API: https://receitas-fit-api.onrender.com

> O plano gratuito do Render pode levar até 50 segundos para acordar após inatividade.

## Licença

MIT
