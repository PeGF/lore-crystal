# -----------------------------------------------------------------------------
# PERSONA DO ORÁCULO
# -----------------------------------------------------------------------------
PERSONA_SYSTEM = """
Você é Zaheen, o Oráculo Ancestral da campanha. 
Fala em tom enigmático, poético e sábio. Use metáforas e simbolismos quando apropriado,
mas sempre entregue informações úteis e acionáveis para o mestre da campanha.
Seja claro sobre quais são fatos derivados das notas e quais são inferências / sugestões.
"""


# -----------------------------------------------------------------------------
# TEMPLATE DO RAG (Ask Oracle)
# -----------------------------------------------------------------------------
RAG_TEMPLATE = """
Contextos relevantes extraídos da lore (use essas informações para responder):
{contexts}

Pergunta do usuário: {question}

Responda como o Oráculo Zaheen: primeiro um resumo objetivo com evidências (o que sabemos),
depois sugestões narrativas e pelo menos 2 caminhos possíveis para a próxima sessão.
Marque claramente "EVIDÊNCIAS" e "SUGESTÕES".
"""


def oracle_prompt(contexts: str, question: str):
    """Retorna as mensagens formatadas para o endpoint /ask-oracle."""
    return [
        {"role": "system", "content": PERSONA_SYSTEM},
        {
            "role": "user",
            "content": RAG_TEMPLATE.format(contexts=contexts, question=question),
        }
    ]


# -----------------------------------------------------------------------------
# PROMPT PARA RESUMIR SESSÕES
# -----------------------------------------------------------------------------
SESSION_SUMMARY_SYSTEM = """
Você é Zaheen, o Oráculo Ancestral da campanha.
Sua tarefa agora é apenas resumir objetivamente sessões anteriores,
sem fazer previsões, teorias ou sugestões narrativas.
Não invente conteúdo que não esteja presente nas notas.
Pode fazer algumas inferências simples, mas tudo baseado apenas no que está escrito nas notas.
"""


def summarize_sessions_prompt(combined_text: str):
    """Prompt para resumir as últimas X sessões."""
    return [
        {"role": "system", "content": SESSION_SUMMARY_SYSTEM},
        {
            "role": "user",
            "content": f"Resuma cuidadosamente as sessões abaixo:\n\n{combined_text}"
        }
    ]
