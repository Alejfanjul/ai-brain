#!/usr/bin/env python3
"""
Módulo de limpeza de conteúdo para captura e embeddings.
Remove URLs de tracking, links internos de EPUB, e outros elementos sem valor semântico.

Uso:
    from content_cleaner import clean_content

    texto_limpo = clean_content(texto_sujo)
"""

import re


def clean_content(text: str) -> str:
    """
    Limpa conteúdo removendo elementos sem valor semântico.

    Remove:
    - URLs de tracking (ConvertKit, Substack, click trackers)
    - Links internos de EPUB (.xhtml#, .html#, index_split)
    - Parâmetros UTM de URLs
    - Links de unsubscribe/open tracking
    - Imagens de tracking (1x1 pixels)

    Mantém:
    - URLs legítimas (simplificadas)
    - Conteúdo textual
    - Estrutura markdown
    """

    # 1. Remove blocos de links de tracking de newsletter completos
    # Ex: [Click here](https://f90a918a.click.convertkit-mail2.com/very-long-tracking-url)
    text = re.sub(
        r'\[([^\]]*)\]\(https?://[^\)]*(?:click\.|unsubscribe\.|open\.)[^\)]*convertkit[^\)]*\)',
        r'\1',  # Mantém só o texto do link
        text,
        flags=re.IGNORECASE
    )

    # 2. Remove links de tracking do Substack (redirect e app-link com tokens)
    text = re.sub(
        r'\[([^\]]*)\]\(https?://[^\)]*substack\.com/redirect/[^\)]*\)',
        r'\1',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'\[([^\]]*)\]\(https?://[^\)]*substack\.com/app-link/[^\)]*\)',
        r'\1',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'\[([^\]]*)\]\(https?://open\.substack\.com/[^\)]*\)',
        r'\1',
        text,
        flags=re.IGNORECASE
    )

    # 3. Remove links internos de EPUB
    # Ex: [Chapter 1](ThisIsStrategy_STG001.xhtml#STG001)
    text = re.sub(
        r'\[([^\]]*)\]\([^\)]*\.xhtml[^\)]*\)',
        r'\1',
        text,
        flags=re.IGNORECASE
    )

    # 4. Remove links de navegação de EPUB (index_split, etc)
    text = re.sub(
        r'\[([^\]]*)\]\([^\)]*index_split[^\)]*\.html[^\)]*\)',
        r'\1',
        text,
        flags=re.IGNORECASE
    )

    # 5. Remove links .html# internos genéricos
    text = re.sub(
        r'\[([^\]]*)\]\([^http][^\)]*\.html#[^\)]*\)',
        r'\1',
        text,
        flags=re.IGNORECASE
    )

    # 6. Remove URLs de tracking soltas (não em markdown links)
    tracking_patterns = [
        r'https?://[^\s]*\.click\.convertkit[^\s]*',
        r'https?://[^\s]*\.unsubscribe\.convertkit[^\s]*',
        r'https?://[^\s]*\.open\.convertkit[^\s]*',
        r'https?://[^\s]*substack\.com/redirect/[^\s]*',
        r'https?://[^\s]*\.list-manage\.com/[^\s]*',
        r'https?://[^\s]*\.campaign-archive\.com/[^\s]*',
    ]
    for pattern in tracking_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # 7. Limpa parâmetros UTM de URLs restantes
    text = re.sub(r'(\?|&)utm_[^&\s\)]*', '', text)

    # 8. Remove imagens de tracking (1x1 pixels, tracking beacons)
    text = re.sub(
        r'!\[[^\]]*\]\([^\)]*(?:open\.|track\.|pixel\.|beacon\.)[^\)]*\)',
        '',
        text,
        flags=re.IGNORECASE
    )

    # 8b. Remove imagens de tracking do Substack (eotrx.substackcdn.com, email.mg1.substack.com)
    text = re.sub(
        r'!\[[^\]]*\]\(https?://[^\)]*(?:eotrx\.substackcdn\.com|email\.mg\d*\.substack\.com)[^\)]*\)',
        '',
        text,
        flags=re.IGNORECASE
    )

    # 9. Remove caracteres invisíveis de formatação de email (zero-width, soft hyphens, etc)
    text = re.sub(r'[͏­\u200b\u200c\u200d\ufeff]+', '', text)

    # 9b. Remove linhas que são só espaços invisíveis
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

    # 10. Remove tabelas de layout de email (linhas com muitos | --- | vazios)
    text = re.sub(r'(\|\s*\|\s*)+\|?', '', text)
    text = re.sub(r'(\|\s*---\s*)+\|?', '', text)
    text = re.sub(r'\n\s*\|\s*\n', '\n', text)

    # 11. Remove linhas que são apenas "---" repetidos (separadores EPUB)
    text = re.sub(r'\n-{3,}\n-{3,}\n', '\n---\n', text)

    # 11b. Normaliza separadores múltiplos inline (--- --- ---) para um único ---
    text = re.sub(r'(---\s*){2,}', '---', text)

    # 11c. Remove elementos de UI de email (padrões específicos e seguros)
    ui_patterns = [
        r'\bView in browser\b',
        r'\bREAD IN APP\b',
        r'\bInvite Friends\b',
        r'\bStart writing\b',
        r'\bUnsubscribe\b',
        r'\bSubscribed\b(?!\s+to)',  # "Subscribed" sozinho, não "Subscribed to"
        r'©\s*\d{4}[^\.]*(?:Market Street|PMB)[^\n]*',  # Rodapés com endereço
    ]
    for pattern in ui_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # 11d. Remove blocos de ações sociais (Like/Comment/Restack juntos)
    text = re.sub(r'\bLike\s*---\s*Comment\s*---\s*Restack\b', '', text, flags=re.IGNORECASE)

    # 12. Remove linhas vazias excessivas
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # 13. Remove espaços em branco no início/fim de linhas
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    text = '\n'.join(lines)

    return text.strip()


def clean_file(filepath: str) -> tuple[str, int, int]:
    """
    Limpa um arquivo markdown.

    Returns:
        (conteúdo_limpo, tamanho_original, tamanho_novo)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    cleaned = clean_content(original)

    return cleaned, len(original), len(cleaned)


if __name__ == "__main__":
    # Teste rápido
    test_text = """
# Test Article

Check out this [great link](https://f90a918a.click.convertkit-mail2.com/qduxpvnpq4i7h4qe480ilh820mwkkb39w2leo96pr?very-long-tracking-param=abc123)

And this EPUB link [Chapter 1](ThisIsStrategy_STG001.xhtml#STG001)

Normal URL: https://example.com/article?utm_source=newsletter&utm_medium=email

Real content here.
"""

    print("=== Original ===")
    print(test_text)
    print(f"\nTamanho: {len(test_text)} chars")

    print("\n=== Limpo ===")
    cleaned = clean_content(test_text)
    print(cleaned)
    print(f"\nTamanho: {len(cleaned)} chars")
    print(f"Redução: {100 - len(cleaned)*100//len(test_text)}%")
