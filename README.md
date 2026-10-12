# claude-plugins

Plugins de Claude Code de Franco, reutilizables entre proyectos.

## Instalar
```bash
claude plugin marketplace add francofadini/claude-plugins   # o la ruta local
claude plugin install secrets@francofadini --scope project
```

## Plugins
- **secrets**: secretos encriptados con dotenvx. El agente los usa y los escribe (desde el portapapeles) sin ver nunca el valor. Hooks que bloquean leer `.env` y volcar credenciales al chat. Requiere `dotenvx` y `jq`.
- **idea2spec** (in English): from an app idea to a shape document with sketches the person approves, plus a `spec/` folder ready for an AI to build the app. Built for non-technical people: few questions, the system brings the design judgment (base canon + auditor). Requires `python3` with `playwright`; Mobbin and `cloudflared` optional.

### Try idea2spec without installing
```bash
claude --plugin-dir ~/path/to/claude-plugins/plugins/idea2spec
```
