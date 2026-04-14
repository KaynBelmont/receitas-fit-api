import os
import json
import re
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/auto"

app = FastAPI(title="Receitas Fit API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngredientesRequest(BaseModel):
    ingredientes: List[str]
    preferencias: Optional[str] = ""

def construir_prompt(ingredientes: List[str], preferencias: str) -> str:
    lista_ingredientes = ", ".join(ingredientes)
    pref_texto = f"\nPreferências alimentares: {preferencias}" if preferencias else ""
    return f"""Você é um chef especialista em culinária fit e saudável.
O usuário possui os seguintes ingredientes: {lista_ingredientes}.{pref_texto}
Crie EXATAMENTE 3 receitas fit e saudáveis usando principalmente esses ingredientes.
Responda SOMENTE com um JSON válido, sem markdown, sem texto extra:
{{
  "receitas": [
    {{
      "nome": "Nome da Receita",
      "tempo_preparo": "20 minutos",
      "porcoes": 2,
      "calorias_por_porcao": 350,
      "ingredientes": ["200g de frango", "1 xícara de arroz integral"],
      "modo_preparo": ["Passo 1: ...", "Passo 2: ..."],
      "dica_fit": "Dica nutricional.",
      "macros": {{
        "proteinas": "30g",
        "carboidratos": "45g",
        "gorduras": "8g",
        "fibras": "5g"
      }}
    }}
  ],
  "mensagem": "Mensagem motivacional curta."
}}"""

@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API de Receitas Fit rodando!"}

@app.post("/receitas")
async def gerar_receitas(request: IngredientesRequest):
    if not request.ingredientes:
        raise HTTPException(status_code=400, detail="Informe pelo menos 1 ingrediente.")
    if len(request.ingredientes) > 20:
        raise HTTPException(status_code=400, detail="Máximo de 20 ingredientes.")

    prompt = construir_prompt(request.ingredientes, request.preferencias or "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://fitchef.app",
        "X-Title": "FitChef AI"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        texto = data["choices"][0]["message"]["content"].strip()
        texto = re.sub(r"```json\n?", "", texto)
        texto = re.sub(r"```\n?", "", texto)
        dados = json.loads(texto.strip())
        return dados

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erro ao processar resposta da IA. Tente novamente.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/ingredientes/sugestoes")
def sugerir_ingredientes():
    return {
        "proteinas": ["frango", "atum", "ovo", "carne moída", "tofu", "grão de bico"],
        "carboidratos": ["arroz integral", "batata doce", "aveia", "quinoa", "mandioca"],
        "legumes": ["brócolis", "espinafre", "cenoura", "abobrinha", "couve", "tomate"],
        "frutas": ["banana", "maçã", "morango", "abacate", "limão"],
        "outros": ["azeite", "alho", "cebola", "gengibre", "cúrcuma", "canela"]
    }