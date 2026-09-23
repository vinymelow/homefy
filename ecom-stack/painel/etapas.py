"""Registo de etapas do pipeline e execução de cada tipo de job.

Cada etapa aparece como um botão na ficha do produto (`/p/<slug>`).
Etapas de agente correm `kimi -p --auto` no repo; etapas de API correm
código Python direto (geradores.py).
"""
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def prompt_pagina_vendas(slug):
    return (
        f"Lê o ficheiro research/landers/{slug}-brief.md (brief completo do produto) e executa "
        f"exatamente o método descrito em prompts/pagina-vendas.md para gerar a landing page "
        f"desse produto. Usa templates/landing-page.html como base. Guarda o resultado final em "
        f"templates/{slug}.html. Respeita os guardrails do brief (secção 7) — preços, garantias "
        f"e claims por confirmar ficam como placeholders editáveis, nunca inventados. "
        f"NÃO publiques nada na Shopify. No fim resume: ficheiros criados e placeholders pendentes."
    )

# tipo → (rótulo no botão, descrição curta, pago?, custo estimado p/ exibir)
ETAPAS = {
    "pagina_vendas": ("Gerar página de vendas", "Copy + HTML da landing page (agente, usa prompts/pagina-vendas.md)", False, None),
    "video_higgsfield": ("Gerar vídeo 9:16 (Higgsfield)", "Vídeo UGC de ~5s com áudio via Seedance 2.0", True, "~$0.50"),
}

def executar(tipo, meta, logf):
    if tipo == "pagina_vendas":
        _agente(prompt_pagina_vendas(meta["slug"]), logf, timeout=1800)
    elif tipo == "video_higgsfield":
        from . import geradores
        geradores.higgsfield_video(meta, logf)
    else:
        raise ValueError(f"Tipo de job desconhecido: {tipo}")

def _kimi_bin():
    caminho = shutil.which("kimi") or "/root/.kimi-code/bin/kimi"
    if not os.path.exists(caminho):
        raise RuntimeError("Binário kimi não encontrado")
    return caminho

def _agente(prompt, logf, timeout=1800):
    logf.write("$ kimi -p <prompt>\n")
    logf.flush()
    proc = subprocess.Popen(
        [_kimi_bin(), "-p", prompt],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
        env={**os.environ})
    try:
        saida, _ = proc.communicate(timeout=timeout)
        logf.write(saida or "(sem output)")
        logf.flush()
    except subprocess.TimeoutExpired:
        proc.kill()
        raise RuntimeError(f"Agente excedeu o tempo limite ({timeout}s)")
    if proc.returncode != 0:
        raise RuntimeError(f"Agente terminou com código {proc.returncode} — ver log")
