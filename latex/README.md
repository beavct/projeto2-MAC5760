# Projeto 2 — Artigo SBC (MAC0426 / MAC5760)

**Tema:** Overhead de Operações Criptográficas em Bancos de Dados Distribuídos
**Grupo:** Beatriz Viana Costa, Lys Katherine Park Kang, Raphaella Brandão Jacques, Stephanie Maria Braga
**Entrega:** 28/06/2026 · **Apresentação:** 23–25/06/2026

## Arquivos

| Arquivo | O que é |
|---|---|
| `main.tex` | Artigo. Esqueleto com as 8 seções; comentários `% GUIA:` dizem o que entra em cada uma e a qual item do enunciado corresponde; `% [PREENCHER]` marca o que falta. |
| `referencias.bib` | Referências iniciais (todas reais). Conferir e ampliar com fontes do experimento. |
| `sbc-template.sty` | Estilo oficial SBC (conferências). **Não editar.** |
| `caption2.sty`, `sbc.bst` | Dependências do template (estilo de legendas e de bibliografia). **Não editar.** |
| `figuras/` | Gráficos/imagens do experimento (`.pdf` ou `.png`). |

## Compilar no Overleaf (recomendado pelo enunciado)

1. Em overleaf.com → **New Project → Upload Project** e suba **todos** os arquivos desta pasta (ou um `.zip` dela).
2. Em **Menu → Settings**, compilador = **pdfLaTeX**, *Main document* = `main.tex`.
3. **Recompile**. O BibTeX roda sozimo no Overleaf; basta recompilar 2x para as citações aparecerem.

> Alternativa: abrir o [template SBC oficial no Overleaf](https://www.overleaf.com/latex/templates/sbc-conferences-template/blbxwjwzdngr) e substituir o `main.tex` dele pelo nosso + subir o `referencias.bib`.

## Compilar localmente

Requer uma distribuição LaTeX (TeX Live / MacTeX). Não há LaTeX instalado nesta máquina ainda — instalar com `brew install --cask mactex-no-gui` (ou `basictex`).

```
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

Gera `main.pdf`. (As três passadas + bibtex são necessárias para resolver citações e referências cruzadas.)

## Mapa enunciado → seções

| Item do enunciado | Seção |
|---|---|
| 1. Contextualização e motivação | Introdução |
| 2. Objetivos | Introdução (perguntas de pesquisa) |
| 3. Métodos | Metodologia |
| 4. Principais conceitos | Conceitos Fundamentais |
| 5. Estado da arte (teoria + ferramentas) | Trabalhos Relacionados |
| 6. Estudo realizado + resultados | Experimentos e Resultados |
| 7. Discussão | Discussão |

## Pendências do grupo

- **SGBD do experimento** ainda não definido (esqueleto está agnóstico). Candidatos livres: CockroachDB, YugabyteDB, MongoDB, Cassandra.
- Preencher e-mails reais em `main.tex`.
- Confirmar nível do grupo (graduação MAC0426 × pós MAC5760) — o enunciado exige grupo homogêneo.
