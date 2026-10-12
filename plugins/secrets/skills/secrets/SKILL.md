---
name: secrets
description: Usar, guardar y listar secretos (API keys, tokens, URIs de DB) con dotenvx sin ver nunca su valor. Usar SIEMPRE que haga falta una credencial, el usuario pase una key o pida configurar variables de entorno, o un comando necesite un token.
---

# secrets · credenciales sin leerlas

Los secretos viven **encriptados con dotenvx**. Por defecto en `.claude/.env` del proyecto; su key, en `.claude/.env.keys`, que nunca se commitea. Cada sub-repo puede tener su propio archivo (ej. `travelapp-back/.env`), que se pasa como `[archivo]`.

Script: `secrets.sh` = `${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/secrets.sh` (usar la ruta completa).

## Regla de oro
El valor de un secreto **nunca** pasa por el chat: no se imprime, no se lee el archivo y no se pide que el usuario lo pegue en el chat. Los hooks del plugin bloquean `cat .env`, `source .env`, `printenv`, `echo $TOKEN`, `dotenvx get` sin nombre y `dotenvx decrypt --stdout`.

## Guardar un secreto nuevo
1. Pedile al usuario: "Copiá el valor de `NOMBRE` al portapapeles y avisame". **No** que lo pegue en el chat.
2. `secrets.sh set NOMBRE [archivo]`: toma el portapapeles, lo guarda encriptado y vacía el portapapeles.
3. Si el usuario igual lo pegó en el chat, avisale que conviene rotarlo.

## Usar un secreto
- En un comando, asignado sin imprimir: `TOKEN=$(dotenvx get RAILWAY_TOKEN -f .claude/.env) && railway ... --token "$TOKEN"`
- Para correr algo con todo cargado: `secrets.sh run [archivo] -- pnpm dev`
- ¿Existe?: `secrets.sh has NOMBRE [archivo]`
- ¿Qué hay?: `secrets.sh names [archivo]` (solo nombres)

## Proyecto nuevo
`secrets.sh init [archivo]` crea el archivo encriptado y suma su `.env.keys` al `.gitignore`. El `.env` encriptado sí se puede commitear; la `.env.keys` jamás. Respaldá la `.env.keys` en tu gestor de contraseñas: sin ella, los secretos no se recuperan.

## Prod
Los secretos de prod van en el proveedor (variables de Railway, secrets de EAS), no acá. Para cargarlos, se usan con `$(dotenvx get ...)` como argumento del CLI del proveedor, nunca impresos.
