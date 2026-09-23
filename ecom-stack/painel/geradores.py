"""Chamadas diretas a APIs de geração de mídia (etapas-API do pipeline).

Por agora: vídeo Higgsfield (Seedance 2.0). Picsart entra na Fase 2 no mesmo
slot — basta implementar picsart_video()/picsart_imagem() e registar a etapa.
"""
import json
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.higgsfield.ai"

def _env():
    env = {}
    path = os.path.join(ROOT, "config", ".env")
    if os.path.exists(path):
        for line in open(path):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

def _req(metodo, url, headers, payload=None, timeout=60):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=metodo, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def higgsfield_video(meta, logf, duracao=5):
    env = _env()
    kid, secret = env.get("HF_API_KEY_ID"), env.get("HF_API_KEY_SECRET")
    if not kid or not secret:
        raise RuntimeError("Faltam HF_API_KEY_ID / HF_API_KEY_SECRET no config/.env")
    slug = meta["slug"]
    prompt_video = meta.get("prompt_video") or meta.get("headline") or slug
    headers = {"Authorization": f"Key {kid}:{secret}", "Content-Type": "application/json"}

    logf.write(f"POST {API}/bytedance/seedance-2.0/text-to-video | slug={slug} | {duracao}s | 9:16\n")
    logf.flush()
    job = _req("POST", f"{API}/bytedance/seedance-2.0/text-to-video", headers, {
        "prompt": prompt_video,
        "resolution": "720p",
        "generate_audio": True,
        "duration": duracao,
        "aspect_ratio": "9:16",
    })
    logf.write(f"resposta: {_resumo(job)}\n")
    jid = job.get("id") or job.get("job_id")
    if not jid:
        raise RuntimeError(f"API não devolveu id de job: {_resumo(job)}")

    destino = os.path.join(ROOT, "assets", "creatives", slug)
    os.makedirs(destino, exist_ok=True)
    caminho = os.path.join(destino, f"ugc-video-{int(time.time())}.mp4")

    for tentativa in range(60):  # até ~10 min
        time.sleep(10)
        status = _req("GET", f"{API}/jobs/{jid}", headers)
        st = status.get("status", "?")
        logf.write(f"poll {tentativa+1}: status={st}\n")
        logf.flush()
        if st in ("succeeded", "completed", "success"):
            url = (status.get("output_url") or status.get("video_url")
                   or (status.get("outputs") or [{}])[0].get("url"))
            if not url:
                raise RuntimeError(f"Job concluído mas sem URL de output: {_resumo(status)}")
            urllib.request.urlretrieve(url, caminho)
            logf.write(f"guardado: {caminho}\n")
            return caminho
        if st in ("failed", "error", "cancelled"):
            raise RuntimeError(f"Job falhou: {_resumo(status)}")
    raise RuntimeError("Timeout: job não terminou em 10 minutos")

def _resumo(d):
    try:
        return json.dumps(d, ensure_ascii=False)[:400]
    except Exception:
        return str(d)[:400]
