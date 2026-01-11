#!/usr/bin/env python3
"""
Limpa arquivos existentes em sources/ removendo URLs de tracking e links internos.

Uso:
    python3 scripts/cleanup_sources.py              # Dry-run (mostra o que faria)
    python3 scripts/cleanup_sources.py --apply      # Aplica as mudanças
    python3 scripts/cleanup_sources.py --file X.md  # Limpa arquivo específico
"""

import argparse
import sys
from pathlib import Path

# Importa o módulo de limpeza
sys.path.insert(0, str(Path(__file__).parent))
from content_cleaner import clean_content

SOURCES_DIR = Path(__file__).parent.parent / "sources"


def analyze_file(filepath: Path) -> dict:
    """Analisa um arquivo e retorna estatísticas de limpeza."""
    original = filepath.read_text(encoding='utf-8')
    cleaned = clean_content(original)

    return {
        'filepath': filepath,
        'original_size': len(original),
        'cleaned_size': len(cleaned),
        'reduction': len(original) - len(cleaned),
        'reduction_pct': round((1 - len(cleaned) / len(original)) * 100, 1) if original else 0,
        'changed': original != cleaned,
        'cleaned_content': cleaned
    }


def main():
    parser = argparse.ArgumentParser(description='Limpa arquivos em sources/')
    parser.add_argument('--apply', action='store_true',
                        help='Aplica as mudanças (sem isso, apenas mostra)')
    parser.add_argument('--file', type=str,
                        help='Limpa arquivo específico')
    parser.add_argument('--min-reduction', type=int, default=100,
                        help='Só mostra arquivos com redução mínima de N chars (default: 100)')
    args = parser.parse_args()

    if args.file:
        # Modo arquivo específico
        filepath = SOURCES_DIR / args.file if not Path(args.file).is_absolute() else Path(args.file)
        if not filepath.exists():
            print(f"Arquivo não encontrado: {filepath}")
            sys.exit(1)

        result = analyze_file(filepath)

        print(f"Arquivo: {filepath.name}")
        print(f"Original: {result['original_size']:,} chars")
        print(f"Limpo: {result['cleaned_size']:,} chars")
        print(f"Redução: {result['reduction']:,} chars ({result['reduction_pct']}%)")

        if args.apply and result['changed']:
            filepath.write_text(result['cleaned_content'], encoding='utf-8')
            print("Mudanças aplicadas!")
        elif result['changed']:
            print("\nUse --apply para aplicar as mudanças")

        return

    # Modo todos os arquivos
    print("=== Analisando sources/ ===\n")

    files = sorted(SOURCES_DIR.glob("*.md"))
    results = []

    for f in files:
        result = analyze_file(f)
        if result['changed'] and result['reduction'] >= args.min_reduction:
            results.append(result)

    if not results:
        print(f"Nenhum arquivo precisa de limpeza (mínimo: {args.min_reduction} chars)")
        return

    print(f"Arquivos que precisam de limpeza (redução >= {args.min_reduction} chars):\n")

    total_reduction = 0
    for r in sorted(results, key=lambda x: -x['reduction']):
        print(f"  {r['filepath'].name[:60]:<60}")
        print(f"    {r['original_size']:>8,} -> {r['cleaned_size']:>8,} chars  (-{r['reduction']:,}, {r['reduction_pct']}%)")
        total_reduction += r['reduction']

    print(f"\n{'='*70}")
    print(f"Total: {len(results)} arquivos, {total_reduction:,} chars a remover")

    if args.apply:
        print("\nAplicando mudanças...")
        for r in results:
            r['filepath'].write_text(r['cleaned_content'], encoding='utf-8')
            print(f"  Limpo: {r['filepath'].name}")
        print(f"\nMudanças aplicadas a {len(results)} arquivos")
    else:
        print("\n💡 Execute com --apply para aplicar as mudanças")


if __name__ == "__main__":
    main()
