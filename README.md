# claude-plugins

Plugins de Claude Code de Franco, reutilizables entre proyectos.

## Instalar
```bash
claude plugin marketplace add francofadini/claude-plugins   # o la ruta local
claude plugin install secrets@francofadini --scope project
```

## Plugins
- **secrets**: secretos encriptados con dotenvx. El agente los usa y los escribe (desde el portapapeles) sin ver nunca el valor. Hooks que bloquean leer `.env` y volcar credenciales al chat. Requiere `dotenvx` y `jq`.
