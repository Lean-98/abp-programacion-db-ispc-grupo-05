#!/usr/bin/env bash
# Script de respaldo (backup) de la base de datos Turnero.
#
# Corre pg_dump DENTRO del contenedor de Docker (no hace falta tener
# instalado el cliente de PostgreSQL en la máquina), y guarda el
# resultado en docs/backups/, con fecha y hora en el nombre del archivo.
#
# Uso:
#   ./docs/backup.sh            (desde cualquier carpeta del repo)
#
# Para restaurar un backup en una base nueva:
#   docker compose exec -T db psql -U turnero -d turnero < docs/backups/turnero_<fecha>.sql

set -euo pipefail

DB_USER="${POSTGRES_USER:-turnero}"
DB_NAME="${POSTGRES_DB:-turnero}"
SERVICE="db"

# Se ubica la raíz del repo (carpeta padre de docs/) para que el
# script funcione sin importar desde dónde se lo invoque.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$SCRIPT_DIR/backups"

mkdir -p "$BACKUP_DIR"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
ARCHIVO="$BACKUP_DIR/turnero_${TIMESTAMP}.sql"

cd "$REPO_ROOT"

echo "Generando backup de la base '$DB_NAME'..."
docker compose exec -T "$SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME" --no-owner --no-privileges > "$ARCHIVO"

echo "Backup guardado en: $ARCHIVO"
