"""Etapas do cockpit; toda execução de agente passa pelo executor Hermes."""
import json, os, subprocess, tempfile
from . import settings

REPO_ROOT=str(settings.REPO_ROOT); EXECUTOR=os.path.join(REPO_ROOT,"workflows","executors","hermes-exec.sh")
ETAPAS={"pagina_vendas":("Gerar página de vendas","Copy + HTML local via Hermes; nunca publica",False,None),"video_higgsfield":("Gerar vídeo 9:16 (Higgsfield)","Vídeo UGC de ~5s via API",True,"~$0.50")}
WORKFLOWS={"product-to-page":"Produto → Página","product-to-launch":"Produto → Lançamento (sem publicar)","page-optimization":"Otimização CRO"}

def executar(tipo,meta,logf):
    if tipo=="pagina_vendas":
        slug=meta["slug"]; prompt=f"Leia ecom-stack/research/landers/{slug}-brief.md e execute ecom-stack/prompts/pagina-vendas.md. Use ecom-stack/templates/landing-page.html e grave em ecom-stack/templates/{slug}.html. Respeite os guardrails; não invente preços, garantias, provas ou claims. NÃO publique na Shopify. Resuma arquivos e placeholders."
        return _hermes(prompt,f"page-{slug}",logf,60)
    if tipo=="chat":
        prompt="Você é o assistente operacional do Homefy. Responda em português com objetividade. Este canal não autoriza publicar, gastar, fazer push ou alterar serviços externos; peça aprovação pelo cockpit quando necessário.\n\n"+meta["message"]
        return _hermes(prompt,f"chat-{meta['chat_id']}",logf,20,"web,memory")
    if tipo.startswith("workflow:"):
        workflow=tipo.split(":",1)[1]
        if workflow not in WORKFLOWS: raise ValueError("Workflow desconhecido")
        slug=meta["slug"]; prompt=f"Execute squads/ecommerce-growth/workflows/{workflow}.yaml para '{slug}', usando ecom-stack/research/landers/{slug}-brief.md como contrato. Siga tasks, gates, limites e checklists. Grave apenas artefatos locais. NÃO publique, não faça push, não altere Shopify/Meta/TikTok e não use serviços pagos. Resuma steps, artefatos e bloqueios."
        return _hermes(prompt,f"{workflow}-{slug}",logf,60,"terminal,file,web")
    if tipo=="video_higgsfield":
        from . import geradores
        geradores.higgsfield_video(meta,logf); return {"status":"SUCCESS"}
    raise ValueError(f"Tipo de job desconhecido: {tipo}")

def _hermes(prompt,slug,logf,timeout=20,toolsets="terminal,file"):
    if not os.path.isfile(EXECUTOR): raise RuntimeError("Executor Hermes não encontrado")
    prompt_dir=settings.STATE_DIR/"prompts"; prompt_dir.mkdir(parents=True,exist_ok=True)
    fd,prompt_path=tempfile.mkstemp(prefix=f"{slug}-",suffix=".md",dir=prompt_dir,text=True)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as handle: handle.write(prompt)
        cmd=[EXECUTOR,"-t",slug[:120],"-f",prompt_path,"-d",REPO_ROOT,"-T",str(timeout),"--toolsets",toolsets,"--reasoning",settings.HERMES_REASONING]
        if settings.HERMES_MODEL: cmd += ["--model",settings.HERMES_MODEL]
        if settings.HERMES_PROVIDER: cmd += ["--provider",settings.HERMES_PROVIDER]
        logf.write("$ hermes-exec.sh -f <private-prompt>\n")
        proc=subprocess.run(cmd,cwd=REPO_ROOT,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=(timeout+2)*60); logf.write(proc.stdout); logf.write(proc.stderr)
        fields={}
        for line in proc.stdout.splitlines():
            if "=" in line:
                key,value=line.split("=",1)
                if key in {"STATUS","RUN_DIR","RESULT_JSON","OUTPUT","EXIT_CODE"}: fields[key]=value
        result={}
        if fields.get("RESULT_JSON") and os.path.isfile(fields["RESULT_JSON"]):
            with open(fields["RESULT_JSON"],encoding="utf-8") as handle: result=json.load(handle)
        output=""
        if fields.get("OUTPUT") and os.path.isfile(fields["OUTPUT"]):
            with open(fields["OUTPUT"],encoding="utf-8",errors="replace") as handle: output=handle.read()
        status=str(result.get("status") or fields.get("STATUS") or "FAILED").upper(); usage=result.get("usage") or {}; cost=usage.get("estimated_cost_usd") or usage.get("cost_usd") or 0
        if status not in ("SUCCESS","PARTIAL"): raise RuntimeError(f"Hermes terminou com status {status}")
        return {"status":status,"run_dir":fields.get("RUN_DIR"),"output":output,"cost_usd":cost}
    finally:
        try: os.unlink(prompt_path)
        except OSError: pass
